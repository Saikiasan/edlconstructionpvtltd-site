# EDL Construction Pvt Ltd — Government Portal Architecture & Operations Guide

> **Official Document Ref**: `EDL-DOC-GOV-OPS-2026-V1`  
> **Release Date**: August 2026  
> **Target Audiences**: DevOps Engineers, Frontend Developers, Site Administrators, and Government Liaison Nodal Officers.

---

## 1. Executive Summary & Session Overview

This document provides a comprehensive operational guide for the **Government & Public Sector Infrastructure EPC Subdomain Portal** created for **EDL Construction Pvt Ltd**. 

The portal serves as an authoritative, high-compliance public procurement and project monitoring gateway tailored specifically for:
* **Central Ministries** (Ministry of Road Transport & Highways — MoRTH, Ministry of Housing and Urban Affairs — MoHUA)
* **National & State Highway Authorities** (NHAI, State PWDs)
* **Urban Transit Boards** (Metro Rail Corporations, Indian Railways)
* **Municipal Corporations & Smart City SPVs**
* **Project Management Consultants (PMCs) and Quality Monitors**

```
                    ┌─────────────────────────────────────────────────────────┐
                    │               EDL CONSTRUCTION PVT LTD                  │
                    │        "NATION BUILDING THROUGH RESILIENT INFRASTRUCTURE"│
                    └────────────────────────────┬────────────────────────────┘
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   │                                                           │
                   ▼                                                           ▼
    ┌───────────────────────────────┐                           ┌───────────────────────────────┐
    │     CORPORATE MAIN PORTAL     │                           │   GOVERNMENT EPC SUBDOMAIN    │
    │   edlconstructionpvtltd.in    │ ◄─── Bi-Directional ───►  │  gov.edlconstructionpvtltd.in │
    │   edl-construction.pages.dev  │         Navigation        │ gov-edl-construction.pages.dev│
    └───────────────────────────────┘                           └───────────────────────────────┘
```

---

## 2. Live Production Endpoints

| Environment | Production URL | Primary Function |
| :--- | :--- | :--- |
| **Dedicated Government Portal** | [**`https://gov-edl-construction.pages.dev`**](https://gov-edl-construction.pages.dev) | Standalone public sector infrastructure subdomain with root rewrite (`/` ➔ `/gov`). |
| **Corporate Portal (Gov Gateway)** | [**`https://edl-construction.pages.dev/gov`**](https://edl-construction.pages.dev/gov) | Integrated route inside the primary corporate platform. |
| **Live Main Corporate Website** | [**`https://edl-construction.pages.dev`**](https://edl-construction.pages.dev) | Flagship corporate portfolio, residential/commercial verticals & VIP visit scheduler. |

---

## 3. Directory & File Inventory

```text
d:/Codes/Web/EDL-Construction-Site/
├── docs/
│   ├── ARCHITECTURE.md                  # Corporate site architecture & design system
│   ├── BUSINESS_OVERVIEW.md             # Corporate identity & business verticals
│   └── GOVERNMENT_PORTAL_AND_OPERATIONS.md # [THIS FILE] Government operations manual
├── public/
│   ├── _redirects                       # Cloudflare Pages URL rewrite rule (/ /gov 200)
│   ├── logo.jpeg                        # High-resolution corporate emblem
│   └── favicon.jpeg                     # Official browser favicon
├── src/
│   ├── components/
│   │   ├── Header.astro                 # Corporate header (with Govt Portal badges)
│   │   ├── Footer.astro                 # Corporate footer (with Govt Portal links)
│   │   └── gov/
│   │       ├── GovHeader.astro          # Institutional header with GeM/CVC badges & IST clock
│   │       ├── GovFooter.astro          # Institutional footer with 24x7 disaster hotline
│   │       ├── TenderBoard.astro        # Filterable live tender notice board & NIT downloads
│   │       ├── EmpanelmentGrid.astro    # Class-1 CPWD/NHAI/MoRTH statutory badges
│   │       └── GovProjectCard.astro     # Public infrastructure cards with IRC/IS code specs
│   ├── layouts/
│   │   ├── Layout.astro                 # Corporate layout
│   │   └── GovLayout.astro              # Institutional layout with deep-navy/gold palette
│   └── pages/
│       ├── gov/
│       │   ├── index.astro              # Main Government Portal Landing (/gov)
│       │   ├── tenders.astro            # E-Tenders & EOI Submissions Portal (/gov/tenders)
│       │   ├── infrastructure.astro     # Public Works Portfolio & Machinery (/gov/infrastructure)
│       │   ├── compliance.astro         # CVC Vigilance & 7-Tier QA/QC Matrix (/gov/compliance)
│       │   ├── telemetry.astro          # Live Public Works Telemetry (/gov/telemetry)
│       │   └── liaison.astro            # Ministry & Nodal Officer Desk (/gov/liaison)
│       └── index.astro                  # Corporate homepage
└── package.json                         # NPM scripts, Astro & Wrangler dependencies
```

---

## 4. Command & Operations Guide (CLI Reference)

All commands should be executed from the project root directory (`d:\Codes\Web\EDL-Construction-Site`).

### 4.1 Local Development

To start the Astro development server in background mode per project standards:

```bash
# Start development server in background
astro dev --background

# Inspect background server status
astro dev status

# Stream live development logs
astro dev logs

# Stop the background server
astro dev stop
```

Alternatively, run in the foreground:
```bash
npm run dev
```
*Access local corporate portal*: `http://localhost:4321`  
*Access local government portal*: `http://localhost:4321/gov`

---

### 4.2 Building for Production

Compile all 16 static pages and assets into the `dist/` directory:

```bash
npm run build
```

To preview the compiled `dist/` bundle locally:
```bash
npm run preview
```

---

### 4.3 Cloudflare Pages Production Deployment

Deployments are handled directly via Cloudflare Wrangler CLI.

#### Deploying Dedicated Government Portal (`gov-edl-construction`)
```bash
npx wrangler pages deploy dist --project-name=gov-edl-construction --branch=main
```

#### Deploying Main Corporate Portal (`edl-construction`)
```bash
npx wrangler pages deploy dist --project-name=edl-construction --branch=main
```

#### Single-Line Build & Dual Deployment (Recommended for Releases)
```bash
npm run build && npx wrangler pages deploy dist --project-name=gov-edl-construction --branch=main && npx wrangler pages deploy dist --project-name=edl-construction --branch=main
```

---

## 5. Custom Subdomain & DNS Configuration

To bind your official domain `gov.edlconstructionpvtltd.in` to the production deployment:

### Step 1: Add DNS CNAME Record
In your domain registrar's DNS management console (or Cloudflare DNS):

| Type | Name / Host | Target / Destination | TTL | Proxy Status |
| :--- | :--- | :--- | :--- | :--- |
| `CNAME` | `gov` | `gov-edl-construction.pages.dev` | Auto | Proxied (Orange Cloud) |

### Step 2: Bind Domain in Cloudflare Dashboard
1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com).
2. Navigate to **Workers & Pages** ➔ **`gov-edl-construction`**.
3. Select **Custom domains** tab ➔ Click **Set up a custom domain**.
4. Enter: `gov.edlconstructionpvtltd.in`.
5. Click **Continue** and confirm activation. Cloudflare will automatically provision a free SSL/TLS certificate.

---

## 6. Government Portal Feature Matrix

### 6.1 Institutional Header & Disclosures (`GovHeader.astro`)
* **Live Badges**: Empanelled Class-1 (Super) EPC Contractor | GeM ID: `GEM-EDL-IN-2026` | CVC Integrity Signatory | ISO 9001:2015 / 14001:2015 / 45001:2018.
* **Live IST Clock**: JavaScript real-time clock synced to `Asia/Kolkata`.
* **Corporate Portal Switcher**: Instant transition to `edlconstructionpvtltd.in`.

### 6.2 E-Tender & EOI Information Desk (`/gov/tenders`)
* **Real-time Filterable Board**: Instant client-side search and category filtering across Highways, Bridges, Metro/Transit, Institutional Complexes, and Smart Water.
* **Statutory Metadata**: Project Estimate, Earned Money Deposit (EMD), Pre-Bid Date, Corrigenda counters, and Submission Deadlines.
* **Digital EOI Submission**: Interactive form capturing GSTIN, GeM Seller ID, scope of interest, and generating automatic reference tracking tokens (`EOI-2026-XXXX`).

### 6.3 Public Infrastructure Engineering Showcase (`/gov/infrastructure`)
* **Heavy Civil Domains**:
  1. *Highways & Expressways*: Pavement Quality Concrete (PQC), automatic slipform paving (IRC:SP:84).
  2. *Bridges & Marine Structures*: 6.4 Km Brahmaputra extradosed bridge, M70 underwater concrete, Zone V seismic base dampeners (IRC:112).
  3. *Metro & Rail Corridors*: Segmental U-girders, elevated stations, ballastless tracks (RDSO/IRS standards).
  4. *Administrative Complexes*: GRIHA 5-Star net-zero secretariats & High Court annexures.
  5. *Smart Water Networks*: 150 MLD distribution + 60 MLD ZLD STPs (CPHEEO norms).
  6. *Strategic & Defense Works*: Border Roads Organisation (BRO) all-weather avalanche snow-shed roads.
* **Heavy Machinery Census**: Real-time fleet audit (Batching plants, slipform pavers, launching gantries, Bauer rotary piling rigs, GPS transit mixers).

### 6.4 Statutory Compliance, QA & CVC Vigilance Matrix (`/gov/compliance`)
* **7-Tier Quality Surveillance Regime**: Raw material validation ➔ Batching SCADA telemetry ➔ Pre-pour rebar clearance ➔ Rheology slump checks ➔ Thermal mass concrete sensors ➔ 28-day digital UTM cube crushing ➔ NDT testing (UPV/Rebound hammer).
* **CVC Integrity & Whistleblower Portal**: Confidential contact lines for the Chief Vigilance Officer (`vigilance@edlconstructionpvtltd.in`).
* **Statutory Registry Disclosure**: CIN, GSTIN, PF/ESIC codes, and NABL testing accreditation numbers.

### 6.5 Public Works Telemetry & Milestone Monitoring (`/gov/telemetry`)
* **Interactive Project Switcher**: Live toggle between major EPC contracts.
* **Physical vs Financial Gauges**: Dynamic progress bars, RFI clearance pass rates (99.4%), and cumulative safe man-hours.
* **NABL Concrete Cube Strength Logs**: Tabular compressive strength logs with pass/fail indicators.
* **LiDAR Drone Survey Telemetry**: Geo-tagged aerial survey reports with flight coordinates and millimeter elevation deviation logs.

### 6.6 Ministry Protocol & Government Liaison Desk (`/gov/liaison`)
* **Authorized Hierarchy Directory**: Direct official channels for Executive Director (EPC) and Chief Vigilance Officer.
* **24x7 Emergency Rapid Response Cell**: Dedicated hotline (`1800-200-EDL-GOV`) for emergency bridge repair, flood mitigation, and corridor restoration.
* **Official Protocol Dispatch Form**: Ministry officials can book technical presentations, pre-bid briefings, and joint site inspections with tracking ticket generation (`GOV-REQ-XXXXXX`).

---

## 7. Maintenance & Content Update Checklist

When adding new government projects or active tenders:

1. **Add Tender Notice**:
   Open [`src/components/gov/TenderBoard.astro`](file:///d:/Codes/Web/EDL-Construction-Site/src/components/gov/TenderBoard.astro) and append an entry to the `tenders` array with `refNo`, `title`, `estValue`, `submissionDeadline`, etc.

2. **Add Infrastructure Project**:
   Open [`src/pages/gov/infrastructure.astro`](file:///d:/Codes/Web/EDL-Construction-Site/src/pages/gov/infrastructure.astro) and append an entry to the `projects` array with `specs`, `progress`, `codeCompliance`, etc.

3. **Update Live Telemetry Data**:
   Open [`src/pages/gov/telemetry.astro`](file:///d:/Codes/Web/EDL-Construction-Site/src/pages/gov/telemetry.astro) and update the `projectData` JavaScript object.

4. **Re-deploy**:
   Execute the deployment command:
   ```bash
   npm run build && npx wrangler pages deploy dist --project-name=gov-edl-construction --branch=main && npx wrangler pages deploy dist --project-name=edl-construction --branch=main
   ```

---

## 8. License & Statutory Rights

© 2026 EDL Construction Pvt Ltd — Public Sector Infrastructure & EPC Division. All rights reserved. Registered under RERA, CPWD Class-1 Special Category, ISO 9001:2015, ISO 14001:2015, and ISO 45001:2018.
