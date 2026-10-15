# Gemini & Imagen Watermark Remover — User Guide

A standalone Python utility designed to automatically detect and eliminate the semi-transparent 4-pointed star watermark added by Google Gemini, Imagen, and similar generative AI video/image models.

---

## Key Features

- **Dual Removal Engines**:
  - `hybrid` (Default): Uses mathematical inverse alpha-blending to reconstruct the original pixel colors and texture detail from beneath the watermark, paired with sub-pixel edge feathering.
  - `inpaint`: Traditional Telea fast-marching inpainting algorithm using an exact astroid geometric mask.
- **Video & Image Support**:
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`
  - **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.m4v`
- **Audio Passthrough**: Retains original audio tracks and sync in videos without re-encoding the audio stream.
- **Temporal Consistency**: Coordinates are locked per video stream to prevent frame-to-frame jitter.
- **Batch Processing**: Accepts single files, directory paths, or glob wildcards.

---

## Prerequisites & Installation

### 1. Python Environment
Install OpenCV and NumPy:
```bash
pip install opencv-python numpy
```

### 2. FFmpeg (Required for Videos)
For processing video files and preserving audio tracks, ensure `ffmpeg` is accessible in your system `PATH`:
- **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via `winget install Gyan.FFmpeg`.
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

Verify installation:
```bash
ffmpeg -version
```

---

## Command Reference

```bash
python scripts/remove_gemini_watermark.py [inputs ...] [options]
```

### CLI Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `inputs` | One or more input paths, directories, or wildcard patterns | *(Required)* |
| `-o, --output` | Target folder to save processed files | Saves alongside originals with `_clean` suffix |
| `-i, --inplace` | Overwrite original input files directly | `False` |
| `-m, --method` | Removal algorithm: `hybrid` or `inpaint` | `hybrid` |
| `-q, --quality` | Output JPEG quality for images (1–100) | `95` |
| `-h, --help` | Display CLI help and options | — |

---

## Usage Examples

### 1. Processing Images

#### Clean a single image
Outputs `render_clean.png`:
```bash
python scripts/remove_gemini_watermark.py render.png
```

#### Clean a folder of images in-place
Overwrites files directly inside the directory:
```bash
python scripts/remove_gemini_watermark.py ./public/frames-v1/ -i
```

#### Pass multiple individual files
Pass multiple files directly separated by spaces:
```bash
python scripts/remove_gemini_watermark.py clip1.mp4 clip2.mp4 frame1.jpg frame2.png
```

#### Clean matching files using wildcards / patterns
```bash
# All JPGs and PNGs matching pattern
python scripts/remove_gemini_watermark.py "./images/*.jpg" "./images/*.png" -o ./cleaned_images/

# Multiple video formats at once
python scripts/remove_gemini_watermark.py *.mp4 *.mov *.webm -i
```

#### Mix files, folders, and wildcards together
```bash
python scripts/remove_gemini_watermark.py ./raw_videos/ extra_clip.mp4 "frames_*.jpg" -o ./export/
```

---

### 2. Processing Videos

#### Clean a video file
Creates `drone_shot_clean.mp4` with audio and framerate preserved:
```bash
python scripts/remove_gemini_watermark.py drone_shot.mp4
```

#### Clean multiple videos into an export directory
```bash
python scripts/remove_gemini_watermark.py ./raw_footage/ -o ./final_cut/
```

#### Replace an existing video in-place
```bash
python scripts/remove_gemini_watermark.py promo_video.mp4 -i
```

---

### 3. Advanced Tuning

#### Using Inpainting Mode
For backgrounds with high noise or complex synthetic patterns where alpha unblending leaves slight traces:
```bash
python scripts/remove_gemini_watermark.py input.mp4 -m inpaint
```

#### High-Quality Image Export
For photography or web banner assets requiring minimal JPEG compression:
```bash
python scripts/remove_gemini_watermark.py photo.jpg -q 99
```

---

## How It Works

The Gemini watermark is an astroid curve defined by:

$$\left|\frac{x - c_x}{r_x}\right|^p + \left|\frac{y - c_y}{r_y}\right|^p \le 1$$

where $p \approx 0.6$. The watermark is composited as a semi-transparent layer:

$$I_{\text{watermarked}} = (1 - \alpha) \cdot I_{\text{original}} + \alpha \cdot W$$

Instead of simply blurring the area, the `hybrid` method solves for $I_{\text{original}}$:

$$I_{\text{original}} = \frac{I_{\text{watermarked}} - \alpha \cdot W}{1 - \alpha}$$

This preserves high-frequency grass, concrete, water, and brick textures underneath the watermark rather than turning them into blurred patches.
