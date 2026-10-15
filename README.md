# EDL Construction Pvt Ltd — Digital Platform & Website

Welcome to the official repository and documentation for the **EDL Construction Pvt Ltd** digital portal.

> **Motto**: *Design • Build • Deliver*  
> **Official Corporate Portal**: [edlconstructionpvtltd.in](https://edlconstructionpvtltd.in)  
> **Headquarters**: EDL Tower, 14th Floor, Senapati Bapat Marg, Lower Parel, Mumbai, Maharashtra 400013

---

## 📚 Project Documentation

Detailed project and business documents are maintained in the [`docs/`](file:///d:/Codes/Web/EDL-Construction-Site/docs) folder:

1. **[Business Overview & Corporate Profile](file:///d:/Codes/Web/EDL-Construction-Site/docs/BUSINESS_OVERVIEW.md)**:
   * Executive summary and brand identity
   * Vision, mission, and core values
   * 4 Core EPC business verticals (Luxury Residential, Commercial, Heavy Civil Infrastructure, Biophilic Green Townships)
   * Flagship landmark portfolio (*The Skygardens*, *EDL Apex*, *Marine Expressway Bridge*, *Solaria Township*)
   * 4-Stage engineering methodology & 7-tier ISO 9001:2015 QA surveillance
   * QHSE & ESG commitments (12.5M+ safe man-hours, GGBS green concrete, closed-loop water treatment)

2. **[Technical Architecture & Platform Documentation](file:///d:/Codes/Web/EDL-Construction-Site/docs/ARCHITECTURE.md)**:
   * Astro 5.x + Tailwind CSS + GSAP ScrollTrigger architecture
   * Detailed directory structure and component breakdown
   * Page-by-page functionality (Cinematic 3D hero, interactive cost drafting workbench, live telemetry tracker)
   * Design system tokens, color palettes, and typography guidelines
   * Development, build, and deployment workflows

3. **[Government Portal Architecture & Operations Guide](file:///d:/Codes/Web/EDL-Construction-Site/docs/GOVERNMENT_PORTAL_AND_OPERATIONS.md)**:
   * Public Sector Infrastructure EPC division specifications (`gov.edlconstructionpvtltd.in`)
   * Live E-Tenders & RFP board, EOI submissions, and GeM/CVC statutory compliance
   * 7-Tier QA/QC concrete testing regime & NABL laboratory surveillance
   * Real-time public works telemetry and Nodal Officer Protocol Desk
   * Production deployment workflows & Cloudflare Pages commands

---

## 🚀 Quick Start & CLI Commands

### Prerequisites
- Node.js `v22.12.0` or higher
- npm

### Installation & Development

```sh
# Install dependencies
npm install

# Start development server in background
astro dev --background

# Inspect background server status
astro dev status

# Check live server logs
astro dev logs

# Stop background server
astro dev stop
```

### Production Build & Deployment

```sh
# Build static production bundle into dist/
npm run build

# Deploy dedicated Government Subdomain (https://gov-edl-construction.pages.dev)
npm run deploy:gov

# Deploy Corporate Portal (https://edl-construction.pages.dev)
npm run deploy:corp

# Build & Deploy to both production endpoints simultaneously
npm run deploy:all

# Preview production build locally
npm run preview
```

---

## 🌟 Key Features

* **Cinematic 3D Hero Animation**: Dual French window casements opening to reveal a vector CAD blueprint on an executive drafting desk.
* **Interactive Area Cost Workbench**: Instant BOQ estimations across residential, commercial, and heavy civil categories.
* **Live RERA & Milestone Telemetry**: Real-time progress trackers with physical completion gauges and statutory compliance stamps.
* **Responsive & Accessible**: Optimized for high-resolution 4K desktops, tablets, and smartphones with fluid responsive typography.

---

## 📄 License & Compliance

© 2026 EDL Construction Pvt Ltd. All rights reserved. Registered under RERA & ISO 9001:2015 Quality Management Standards.
