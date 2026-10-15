#!/usr/bin/env python3
"""
gemini_watermark_remover.py
----------------------------
A standalone, high-performance tool to automatically detect and remove 
Gemini / Imagen 4-pointed star watermarks from images, image directories, 
and video files (.mp4, .mov, .avi, .mkv, .webm).

Features:
- Video & Image Support:
    - Videos: Processes frame-by-frame, preserves original audio track, framerate, and resolution via ffmpeg.
    - Images: Supports single images, wildcard globs, or full recursive directories.
- Watermark Removal Modes:
    1. 'hybrid' (Default): Reverse alpha-unblending to mathematically reconstruct 
       underlying pixel colors & textures + sub-pixel edge feathering.
    2. 'inpaint': Telea fast-marching inpaint across the astroid mask.
- Temporal Stability for Videos:
    - Watermark position is detected once or tracked to prevent frame-to-frame jitter.
- Output Flexibility:
    - Save to target directory, custom output path, or overwrite in-place.

Requirements:
    pip install opencv-python numpy
    (ffmpeg must be installed on your system for video audio passthrough)
"""

import os
import sys
import glob
import shutil
import argparse
import subprocess
from typing import List, Tuple, Optional
import cv2
import numpy as np

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}


def is_video(filepath: str) -> bool:
    return os.path.splitext(filepath)[1].lower() in VIDEO_EXTENSIONS


def is_image(filepath: str) -> bool:
    return os.path.splitext(filepath)[1].lower() in IMAGE_EXTENSIONS


def generate_astroid_mask(radius: int = 32, p: float = 0.6) -> Tuple[np.ndarray, Tuple[int, int]]:
    """Generates an astroid (4-pointed star) mask: |x/r|^p + |y/r|^p <= 1"""
    size = radius * 2 + 10
    cx = size // 2
    cy = size // 2
    y, x = np.ogrid[:size, :size]
    dist = (np.abs(x - cx) / float(radius)) ** p + (np.abs(y - cy) / float(radius)) ** p
    mask = (dist <= 1.05).astype(np.uint8) * 255
    return mask, (cx, cy)


def detect_watermark_location(
    img: np.ndarray,
    search_roi_ratio: Tuple[float, float, float, float] = (0.6, 0.6, 1.0, 1.0)
) -> Tuple[int, int, int]:
    """Detects center (cx, cy) and radius of watermark in the bottom-right quadrant."""
    h, w = img.shape[:2]
    ymin = int(h * search_roi_ratio[0])
    xmin = int(w * search_roi_ratio[1])
    ymax = int(h * search_roi_ratio[2])
    xmax = int(w * search_roi_ratio[3])

    roi = img[ymin:ymax, xmin:xmax]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    base_radius = int(round(32 * (min(w, h) / 720.0)))
    base_radius = max(18, min(60, base_radius))

    best_val = -1
    best_loc = None
    best_r = base_radius

    for r in [base_radius - 4, base_radius, base_radius + 4]:
        template, _ = generate_astroid_mask(radius=r)
        kernel = template.astype(np.float32) / 255.0
        kernel_edges = cv2.Laplacian(kernel, cv2.CV_32F)
        gray_edges = cv2.Laplacian(gray.astype(np.float32), cv2.CV_32F)

        res = cv2.matchTemplate(gray_edges, kernel_edges, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > best_val:
            best_val = max_val
            best_r = r
            best_loc = (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)

    if best_loc is not None and best_val > 0.15:
        abs_cx = xmin + best_loc[0]
        abs_cy = ymin + best_loc[1]
        return abs_cx, abs_cy, best_r

    # Default fallback: standard 90.6% X, 84.1% Y
    fallback_cx = int(w * 0.90625)
    fallback_cy = int(h * 0.84166)
    return fallback_cx, fallback_cy, base_radius


def remove_watermark_from_image(
    img: np.ndarray,
    cx: Optional[int] = None,
    cy: Optional[int] = None,
    radius: Optional[int] = None,
    method: str = "hybrid",
    watermark_brightness: float = 250.0,
    alpha_boost: float = 1.15
) -> np.ndarray:
    """Removes watermark from a single BGR frame."""
    out_img = img.copy()
    h, w = img.shape[:2]

    if cx is None or cy is None or radius is None:
        cx, cy, radius = detect_watermark_location(img)

    pad = radius + 15
    x1 = max(0, cx - pad)
    y1 = max(0, cy - pad)
    x2 = min(w, cx + pad)
    y2 = min(h, cy + pad)

    patch = out_img[y1:y2, x1:x2].astype(np.float32)
    ph, pw = patch.shape[:2]

    local_cx = cx - x1
    local_cy = cy - y1

    y_idx, x_idx = np.ogrid[:ph, :pw]
    dist = (np.abs(x_idx - local_cx) / float(radius)) ** 0.6 + \
           (np.abs(y_idx - local_cy) / float(radius)) ** 0.6

    astroid_mask = (dist <= 1.05).astype(np.uint8) * 255

    if method == "inpaint":
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated_mask = cv2.dilate(astroid_mask, kernel, iterations=1)
        inpainted_patch = cv2.inpaint(out_img[y1:y2, x1:x2], dilated_mask, 3, cv2.INPAINT_TELEA)
        out_img[y1:y2, x1:x2] = inpainted_patch
        return out_img

    # Hybrid Mode: Reverse alpha unblending + edge inpainting
    alpha_profile = np.clip((1.08 - dist) / 0.85, 0.0, 1.0)
    peak_alpha = 0.32 * alpha_boost
    alpha_map = alpha_profile * peak_alpha
    alpha_map[dist > 1.08] = 0.0

    a3 = alpha_map[:, :, np.newaxis]
    restored = (patch - watermark_brightness * a3) / np.maximum(1.0 - a3, 0.05)
    restored = np.clip(restored, 0, 255).astype(np.uint8)

    edge_ring = ((alpha_map >= 0.02) & (alpha_map <= 0.16)).astype(np.uint8) * 255
    edge_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edge_ring = cv2.dilate(edge_ring, edge_kernel, iterations=1)

    cleaned_patch = cv2.inpaint(restored, edge_ring, 2, cv2.INPAINT_TELEA)
    out_img[y1:y2, x1:x2] = cleaned_patch

    return out_img


def remove_watermark_from_video(
    video_path: str,
    output_path: str,
    method: str = "hybrid",
    watermark_brightness: float = 250.0,
    alpha_boost: float = 1.15
) -> bool:
    """
    Processes video frame-by-frame with stable watermark coordinates,
    re-encoding video and preserving original audio via ffmpeg.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[!] Unable to open video: {video_path}")
        return False

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"[*] Processing Video: {os.path.basename(video_path)}")
    print(f"    Resolution: {width}x{height} | FPS: {fps:.2f} | Frames: {total_frames}")

    # Read first frame to detect watermark coordinates stably across the video
    ret, first_frame = cap.read()
    if not ret:
        print("[!] Failed to read video stream.")
        cap.release()
        return False

    cx, cy, radius = detect_watermark_location(first_frame)
    print(f"    Detected watermark at: ({cx}, {cy}), radius: {radius}px")

    # Temporary output for video-only stream
    temp_dir = os.path.dirname(os.path.abspath(output_path))
    temp_video = os.path.join(temp_dir, f"_temp_video_{os.getpid()}.mp4")

    # Use mp4v or H264 for temporary video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    # Process first frame
    frame_cleaned = remove_watermark_from_image(
        first_frame, cx=cx, cy=cy, radius=radius, method=method,
        watermark_brightness=watermark_brightness, alpha_boost=alpha_boost
    )
    writer.write(frame_cleaned)

    frame_idx = 1
    # Process remaining frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        frame_cleaned = remove_watermark_from_image(
            frame, cx=cx, cy=cy, radius=radius, method=method,
            watermark_brightness=watermark_brightness, alpha_boost=alpha_boost
        )
        writer.write(frame_cleaned)

        if total_frames > 0 and frame_idx % max(1, (total_frames // 20)) == 0:
            percent = (frame_idx / total_frames) * 100
            print(f"    Progress: {frame_idx}/{total_frames} frames ({percent:.1f}%)")

    cap.release()
    writer.release()

    # Mux original audio into clean video using ffmpeg
    has_ffmpeg = shutil.which("ffmpeg") is not None
    if has_ffmpeg:
        print("    Muxing original audio and compressing with ffmpeg...")
        # Check if original video has audio stream
        probe_cmd = ["ffmpeg", "-i", video_path]
        probe_res = subprocess.run(probe_cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        has_audio = "Audio:" in probe_res.stderr

        ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_video]
        if has_audio:
            ffmpeg_cmd.extend(["-i", video_path, "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "copy", "-map", "0:v:0", "-map", "1:a:0?"])
        else:
            ffmpeg_cmd.extend(["-c:v", "libx264", "-crf", "18", "-preset", "medium"])
        ffmpeg_cmd.append(output_path)

        run_res = subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(temp_video):
            os.remove(temp_video)
        if run_res.returncode == 0:
            print(f"[+] Video successfully saved: {output_path}")
            return True

    # Fallback if ffmpeg isn't available or fails
    if os.path.exists(output_path):
        os.remove(output_path)
    shutil.move(temp_video, output_path)
    print(f"[+] Video saved: {output_path}")
    return True


def process_paths(
    inputs: List[str],
    output_dir: Optional[str] = None,
    inplace: bool = False,
    method: str = "hybrid",
    jpeg_quality: int = 95
) -> int:
    """Collects and processes all image and video targets."""
    file_list = []
    for item in inputs:
        if os.path.isdir(item):
            for root, _, files in os.walk(item):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
                        file_list.append(os.path.join(root, f))
        elif any(char in item for char in ["*", "?", "["]):
            file_list.extend(glob.glob(item))
        elif os.path.isfile(item):
            file_list.append(item)

    file_list = sorted(list(set(file_list)))
    if not file_list:
        print("[-] No images or videos found matching the inputs.")
        return 0

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    total = len(file_list)
    print(f"[*] Processing {total} file(s). Method: '{method}'")

    for idx, filepath in enumerate(file_list, 1):
        dirname, filename = os.path.split(filepath)
        name, ext = os.path.splitext(filename)

        if inplace:
            out_path = filepath
        elif output_dir:
            out_path = os.path.join(output_dir, filename)
        else:
            out_path = os.path.join(dirname, f"{name}_clean{ext}")

        # Check if video
        if is_video(filepath):
            # For inplace video replacement, output to a temporary clean path then replace
            target_out = out_path
            if inplace:
                target_out = os.path.join(dirname, f"{name}_clean_tmp{ext}")

            ok = remove_watermark_from_video(filepath, target_out, method=method)
            if ok:
                if inplace:
                    os.replace(target_out, filepath)
                success_count += 1
            continue

        # Else image
        try:
            img = cv2.imread(filepath)
            if img is None:
                print(f"[{idx}/{total}] Unable to read: {filepath}")
                continue

            cleaned = remove_watermark_from_image(img, method=method)

            ext_lower = ext.lower()
            if ext_lower in [".jpg", ".jpeg"]:
                cv2.imwrite(out_path, cleaned, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            elif ext_lower == ".png":
                cv2.imwrite(out_path, cleaned, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
            else:
                cv2.imwrite(out_path, cleaned)

            success_count += 1
            if total > 10 and idx % 20 == 0:
                print(f"[*] Processed {idx}/{total} images...")
        except Exception as err:
            print(f"[!] Error processing {filepath}: {err}")

    print(f"\n[+] Successfully completed! Cleaned {success_count}/{total} file(s).")
    return success_count


def main():
    parser = argparse.ArgumentParser(
        description="Automatically remove Gemini / Imagen 4-pointed star watermarks from images and videos."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input image/video files, directories, or glob patterns (e.g. video.mp4, ./frames/, *.jpg)"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Directory to save cleaned files (if not provided, creates _clean files or modifies in-place)"
    )
    parser.add_argument(
        "-i", "--inplace",
        action="store_true",
        help="Overwrite original images/videos in-place"
    )
    parser.add_argument(
        "-m", "--method",
        choices=["hybrid", "inpaint"],
        default="hybrid",
        help="Removal method: 'hybrid' (alpha unblend + edge cleanup, best quality) or 'inpaint' (telea fast marching)"
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=95,
        help="JPEG output quality for images (1-100, default: 95)"
    )

    args = parser.parse_args()

    if not args.inplace and args.output is None:
        print("[i] Note: Neither -o/--output nor -i/--inplace specified.")
        print("    Cleaned files will be saved alongside originals with '_clean' suffix.\n")

    process_paths(
        inputs=args.inputs,
        output_dir=args.output,
        inplace=args.inplace,
        method=args.method,
        jpeg_quality=args.quality
    )


if __name__ == "__main__":
    main()
