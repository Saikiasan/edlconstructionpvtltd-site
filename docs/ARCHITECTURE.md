# EDL Construction Website & Platform — Technical Architecture & Project Documentation

---

## 1. Project Overview

The **EDL Construction Website** is a modern, performance-engineered digital portal designed for **EDL Construction Pvt Ltd**. It showcases the company's architectural mastery, engineering EPC prowess, landmark portfolio, and corporate transparency.

The platform is designed with a **Dark Blueprint / Architectural Drafting Aesthetic** accented with champagne gold (`#C5A059`) and steel navy tones, paired with smooth interactive scrollytelling and telemetry widgets.

---

## 2. Technical Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Framework** | **Astro 5.x** (`astro@^7.2.4`) | Zero-JS default for ultra-fast static HTML generation with islands of interactivity. |
| **Styling** | **Tailwind CSS 3.x** (`@astrojs/tailwind`) | Utility-first styling with custom corporate color palette and typography. |
| **Animation Engine** | **GSAP 3.x + ScrollTrigger** (`gsap@^3.15.0`) | Cinematic 3D French window opening, blueprint unfolding, and parallax storytelling. |
| **Iconography** | **Lucide Icons** (`lucide`) | Crisp, scalable vector icons loaded via CDN/vanilla scripts. |
| **Deployment Target** | Cloudflare Pages / Static Hosting | Blazing fast global edge delivery with instantaneous TTFB. |

---

## 3. Directory & File Structure

```text
EDL-Construction-Site/
├── .vscode/                     # VSCode configuration
├── dist/                        # Production build output
├── docs/                        # Project & business documentation
│   ├── BUSINESS_OVERVIEW.md     # Business profile & corporate identity
│   ├── ARCHITECTURE.md          # Technical stack & design system
│   └── Name Approval Letter...  # Corporate statutory filings
├── public/                      # Static assets (favicons, logos, images)
│   ├── logo.jpeg                # EDL Corporate Logo
│   └── favicon.svg              # Site favicon
├── src/
│   ├── components/
│   │   ├── Header.astro         # Persistent navigation bar with live IST time
│   │   └── Footer.astro         # Corporate footer with statutory disclaimers & sitemap
│   ├── layouts/
│   │   └── Layout.astro         # Root HTML shell with font definitions & global CSS
│   └── pages/
│       ├── index.astro          # Hero sequence, 3D window animation & parallax showcases
│       ├── about.astro          # Corporate identity, engineering methodology & certifications
│       ├── portfolio.astro      # Curated architectural works & project deep dives
│       ├── services.astro       # Turnkey EPC, heavy civil, facade & MEP engineering
│       ├── calculator.astro     # Interactive BOQ cost & built-up area drafting workbench
│       ├── tracker.astro        # Live construction progress & RERA milestone telemetry
│       ├── safety.astro         # QHSE, zero-harm metrics & ESG decarbonization policies
│       ├── careers.astro        # Open engineering, BIM & site management positions
│       └── contact.astro        # VIP site visit scheduling & corporate headquarters info
├── astro.config.mjs             # Astro build & integration configuration
├── package.json                 # NPM scripts & project dependencies
├── tailwind.config.mjs          # Custom theme extensions (fonts, colors, blueprint grids)
├── tsconfig.json                # TypeScript compilation config
├── AGENTS.md                    # Antigravity agent operational rules
├── CLAUDE.md                    # Dev workflow & background server commands
└── README.md                    # Project quick-start & deployment guide
```

---

## 4. Key Pages & Features Breakdown

### 🖥️ 1. Homepage (`src/pages/index.astro`)
* **Cinematic 3D Hero Sequence**:
  * Dual French window casements and velvet drapery opening via GSAP ScrollTrigger timeline.
  * Reveals an architectural drafting desk with a scaled vector SVG elevation blueprint.
  * Embossed official EDL seal with ISO 9001:2015 accreditation stamp.
* **Parallax Storytelling Showcase**:
  * Frame 01: *The Skygardens Residences* (Luxury Residential).
  * Frame 02: *EDL Apex Financial Center* (Grade-A Commercial).
  * Frame 03: *Marine Expressway Bridge & Flyover* (Heavy Civil Infrastructure).
  * Frame 04: *Solaria Green Tech Township* (Biophilic & Solar Microgrid).
* **Interactive Area Cost Estimator**:
  * Live slider adjusting built-up area ($1,000\text{ to }50,000\text{ sq ft}$) with instant INR budget calculation.
* **Accreditations Showcase**:
  * ISO 9001:2015, IGBC Green Building, and RERA compliance badges.

### 📐 2. Interactive Drafting Workbench (`src/pages/calculator.astro`)
* Dynamic client-side calculation script responding to:
  * Category Selection: Residential (`₹2,800/sq.ft`), Commercial (`₹3,400/sq.ft`), Infrastructure (`₹4,200/sq.ft`).
  * Specification Tiers: Standard Luxury ($1.0\times$), Premium Architectural ($1.35\times$), Ultra Bespoke ($1.8\times$).
* Displays realistic turnkey investment ranges in INR Crores.

### 📡 3. Live Project Telemetry (`src/pages/tracker.astro`)
* Displays real-time milestone telemetry across active projects:
  * Piling foundation completion counts.
  * Pier shaft cast metrics.
  * Superstructure and stay-cable tension progress bars.
  * RERA escrow status reconciliation and statutory approvals.

### 🛡️ 4. Safety & ESG Ledger (`src/pages/safety.astro`)
* **12.5M+** Safe Man-Hours counter without Lost Time Injury (LTI).
* 4-Pillar Safety Architecture:
  1. Daily Toolbox Talks & Risk Assessments.
  2. Ground Granulated Blast-Furnace Slag (GGBS) green concrete reduction.
  3. Closed-loop water recycling & mist cannon dust suppression.
  4. Worker occupational health dispensaries and welfare policies.

### 💼 5. Curated Portfolio (`src/pages/portfolio.astro`)
* High-definition visual showcases with project parameters, location coordinates, IGBC/LEED ratings, and blueprint access request CTA.

### 🤝 6. VIP Site Visit Consultation (`src/pages/contact.astro`)
* Interactive consultation booking form with project selection.
* Official headquarters coordinates and corporate NDA availability.

---

## 5. Design System & Typography

```css
/* Color Palette */
--bg-primary: #07090E;       /* Obsidian Blueprint Dark */
--bg-secondary: #090F1D;     /* Navy Drafting Table */
--accent-gold: #C5A059;      /* Champagne Gold Accent */
--accent-gold-hover: #D4AF37;/* Polished Brass */
--slate-border: #1E293B;     /* Technical Grid Line */
```

* **Serif Headings**: *Cinzel* / *Playfair Display* for corporate majesty and timeless elegance.
* **Display / Brand Accent**: *Syne* for bold architectural typography.
* **Monospace Data / Schematics**: *JetBrains Mono* / *Fira Code* for technical telemetry, dimensions, and specifications.
* **Body Prose**: *Plus Jakarta Sans* / *Inter* for clean, modern readability.

---

## 6. Developer Commands & Workflows

```sh
# 1. Install dependencies
npm install

# 2. Launch Astro dev server in background (per AGENTS.md rules)
astro dev --background

# 3. Check status of background server
astro dev status

# 4. View live logs
astro dev logs

# 5. Stop background server
astro dev stop

# 6. Build optimized static production bundle
npm run build

# 7. Preview production build locally
npm run preview
```
