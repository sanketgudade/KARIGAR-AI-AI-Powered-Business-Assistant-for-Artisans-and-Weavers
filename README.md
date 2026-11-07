# KARIGAR AI (कारीगर AI)
### AI-Powered Business Assistant for Artisans and Weavers
> **GAVS / Tech4Bharat Hackathon 2026 · Problem Statement 7.1**  
> *"Empowering Artisans. Preserving Heritage. Building Fair Markets."*  
> **Core Operating Philosophy:** **"AI recommends. Artisans decide."**

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![MySQL 8.0](https://img.shields.io/badge/MySQL-8.0-4479A1.svg?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Lifecycle Tests](https://img.shields.io/badge/Lifecycle_Tests-100%25_PASS-success.svg)](#-automated-verification--test-results)
[![API Tests](https://img.shields.io/badge/API_Tests-8%2F8_PASS-success.svg)](#-automated-verification--test-results)

---

## 📌 Executive Summary

Traditional Indian handloom weavers, terracotta potters, woodcraft artisans, and metalcraft guilds create irreplaceable cultural treasures. Yet, because of deep language barriers, digital divides, and reliance on exploitative middlemen, they capture only a fraction of their craft's true economic value.

**KARIGAR AI** is not an ordinary e-commerce marketplace. It is an **intelligent, multimodal business operating system** built specifically around how traditional artisans naturally communicate:
- **Voice-First in Native Tongues:** Artisans speak in Marathi, Hindi, Tamil, or Telugu; AI transcribes, translates, and generates culturally authentic catalog stories.
- **Scientific Cost Accounting & Living Wage Defense:** Calculates raw materials, skilled labor hours, and fair hourly wages to establish fair listing rates.
- **Confidential Floor Price Protection:** Guards secret minimum acceptable rates with zero data leakage to buyers.
- **Empathetic AI Negotiation Intelligence:** Automatically drafts value-articulating counteroffers justifying labor effort when buyers propose below-floor predatory rates.
- **Sovereign Artisan Authority:** AI only calculates and drafts. No listing is published, no price is set, and no counteroffer is transmitted without explicit human approval.

---

## 🏛 The 4 Specialized AI Agents

```
+----------------------------------------------------------------------------------------------------+
|                                    KARIGAR AI CORE ARCHITECTURE                                    |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|    [ AGENT 1: Story & Catalog ]    --> [ AGENT 2: Market & Costing ]   --> [ AGENT 4: Negotiation ]|
|    * Speech-to-Text (Whisper)          * Cost Accounting (Labor+Mat)       * Below-Floor Threat Flag   |
|    * Indic Translation (Bhashini)      * 5-Listing Regional Benchmark      * Margin Loss Simulation    |
|    * Computer Vision Motifs (CLIP)     * Recommended Listing Price         * Polite Cultural Counter   |
|    * Cultural Storytelling             * Secret Confidential Floor         * Deal Protection           |
|                 │                                      │                                      │     |
|                 ▼                                      ▼                                      ▼     |
|      [ APPROVAL GATE 1 ]                    [ APPROVAL GATE 2 ]                    [ APPROVAL GATE 3 ]      |
|    Artisan Signs Listing                  Artisan Fixes Public & Floor            Artisan Approves Counter  |
|                                                                                                    |
|    <--------------------------- [ AGENT 3: Visual Discovery & RFQ ] -----------------------------> |
|                                 * Reverse Image Vector Matching (CLIP)                             |
|                                 * Multimodal Semantic Retrieval                                    |
|                                 * Buyer RFQ Generation (Zero Floor Leakage)                        |
+----------------------------------------------------------------------------------------------------+
```

### 1. Agent 1: Multimodal Story & Cataloguing Agent (Approval Gate 1)
* **Voice-First & Multilingual:** Artisans speak in regional languages (e.g., Marathi: *"माझं नाव मीना जाधव आहे. मी येवल्यामध्ये पारंपारिक पैठणी विणते..."*).
* **Audio Transcription & Indic Translation:** Integrated with Whisper speech-to-text and Bhashini / IndicTrans translation pipelines.
* **Computer Vision Extraction:** Observes color palettes, detects weave structures, and identifies motifs (e.g., peacock, lotus, asawali) without hallucinating unverified composition claims.
* **Cultural Provenance:** Authors professional, heritage-grounded descriptions in English and native Indic languages.
* **Gate 1 Enforcement:** Listing is held strictly at `DRAFT` status until the artisan reviews and clicks **Approve Listing**.

### 2. Agent 2: Fair Price and Market Intelligence Agent (Approval Gate 2)
* **Production Cost Accounting:** Computes exact cost breakdowns:
  $$\text{Production Cost} = \text{Raw Materials (₹1,500)} + (\text{20 Hours Worked} \times \text{₹50/hr Fair Wage}) + \text{Packaging \ Overheads (₹300)} = \text{₹2,800}$$
* **Regional Market Intelligence:** Automatically scans and indexes 5 verified regional craft listings from portals like *CraftBazaar* and *WeaverStory*, providing real-time Min (₹4,500), Median (₹5,200), and Max (₹6,000) benchmarks.
* **Pricing Recommendations:**
  * **Suggested Public Listing Price:** ₹5,000 (44% gross margin).
  * **Confidential Loss-Prevention Floor:** ₹4,200 (secret reservation price).
* **Gate 2 Enforcement:** Artisan explicitly confirms both the public price and confidential floor before the product transitions to `ACTIVE_MARKET`.

### 3. Agent 3: Visual Discovery & Quotation Agent
* **Reverse Image Vector Matching:** Buyers upload reference craft photographs; Agent 3 computes visual vector embeddings to match products by silhouette, palette, and motif.
* **Confidentiality Shield:** Public buyer API queries completely exclude internal production costs and secret floor prices.
* **Wholesale RFQ Generator:** Generates bulk price estimates and displays artisan loom lead times based on requested quantity.

### 4. Agent 4: Negotiation & Commercial Intelligence Agent (Approval Gate 3)

- **Threat Detection Algorithm:** Instantly compares buyer offers against the artisan's confidential floor price:

  \[
  P_{\text{offer}} < P_{\text{floor}}
  \implies \text{Flag: RED ALERT (BELOW\_CONFIDENTIAL\_FLOOR)}
  \]

- **Comparative Margin Simulator:**
  - At buyer's predatory offer (₹3,000): Weaver earns only ₹200/saree (₹10,000 profit for 50 sarees — subsistence wage).
  - At AI counteroffer (₹4,500): Weaver earns ₹1,700/saree (₹85,000 net profit — healthy 38% commercial margin).

- **Culturally Grounded Counteroffer Message:** Drafts a polite, dignified response explaining that 20 days of pure mulberry silk weaving cannot be sold at ₹3,000, while extending a sustainable wholesale rate of ₹4,500.

- **Gate 3 Enforcement:** Counteroffer will **NEVER** be transmitted autonomously. It remains in `PENDING_ARTISAN` until the artisan clicks **Approve & Transmit**.

---

## 🔒 The 3 Sovereign Approval Gates

| Approval Gate | Stage | Artisan Signing Authority | Status Transition |
|---|---|---|---|
| **Gate 1: Catalogue Sign-Off** | Listing Creation | Verifies photographs, title, Indic translation, and cultural story | `DRAFT` ➔ `APPROVED_LISTING` |
| **Gate 2: Pricing Sign-Off** | Commercial Valuation | Fixes public listing price and private confidential floor | `APPROVED_LISTING` ➔ `ACTIVE_MARKET` |
| **Gate 3: Negotiation Sign-Off**| Buyer Counteroffer | Approves final counteroffer rate and drafted negotiation message | `PENDING_ARTISAN` ➔ `COUNTER_SENT` |

Every gate action is immutably logged in the `approval_logs` database table with the artisan ID, timestamp, action (`APPROVE`, `EDIT`, `REJECT`), and audit details.

---

## 🚀 End-to-End 9-Step Business Lifecycle

```
[1. Artisan Onboarding] ➔ [2. Multimodal Voice Upload] ➔ [3. Gate 1 Catalogue Approval]
          │
          ▼
[4. Gate 2 Pricing Approval] ➔ [5. Visual Discovery & Buyer RFQ] ➔ [6. Below-Floor Threat Flag]
          │
          ▼
[7. Gate 3 Counteroffer Approval] ➔ [8. Buyer Escrow Payment] ➔ [9. 6-Stage Delivery & Payout]
```

1. **Artisan Registration:** Artisan registers in the Yeola cluster with preferred language (Marathi).
2. **Voice-First Story Recording:** Artisan uploads saree photos and speaks in Marathi.
3. **Gate 1 Approval:** Artisan verifies transcript and story; clears Gate 1.
4. **Gate 2 Pricing Approval:** Agent 2 calculates ₹2,800 cost and ₹5,200 median benchmark. Artisan approves ₹5,000 listing price and sets ₹4,200 confidential floor.
5. **Buyer RFQ:** Buyer discovers saree via visual similarity and submits a 50-piece bulk enquiry.
6. **Buyer Below-Floor Offer:** Buyer offers ₹3,000/saree. Agent 4 flags `BELOW_CONFIDENTIAL_FLOOR` and drafts ₹4,500 counteroffer.
7. **Gate 3 Approval:** Artisan inspects the ₹85,000 profit simulation and approves counteroffer transmission.
8. **Buyer Acceptance & Escrow:** Buyer accepts counteroffer and deposits ₹2,25,000 into secure escrow. Order `#ORD-2026-8841` confirmed.
9. **6-Stage Production & Settlement:** Order transitions: *Confirmed $\rightarrow$ Materials Ready $\rightarrow$ Pit-Loom Weaving $\rightarrow$ Quality Inspection $\rightarrow$ Ready to Ship $\rightarrow$ Dispatched $\rightarrow$ Delivered*. Escrow funds are released to the artisan. Total confirmed revenue updates to ₹2,73,000.

---

## 🛠 Complete Technology Stack

| Layer | Technologies | Purpose |
|---|---|---|
| **Frontend UI** | React 18, Babel Standalone | Component-based reactive user interface with zero build breakage |
| **Styling & Design System** | Tailwind CSS (custom `karigar-*` tokens) | High-craft editorial aesthetic inspired by Indian craft brands & Stripe |
| **Typography** | Playfair Display & Plus Jakarta Sans | Editorial serif headings + clean modern fintech numerical metrics |
| **Icons** | Lucide Icons (CDN & SVG) | Crisp, minimalist operational icons |
| **Backend API** | Python 3.10+, Flask 3.0+ | Lightweight RESTful microservices with Application Factory pattern |
| **ORM & DB Layer** | SQLAlchemy 2.0+, PyMySQL | Relational data persistence with strict foreign keys & cascading deletes |
| **Database** | MySQL 8.0 (`Karigar_Ai`) | Relational database on `localhost:3306` with SQLite test compatibility |
| **CORS Middleware** | Flask-CORS | Secure cross-origin resource sharing between UI and API |
| **Speech-to-Text** | OpenAI Whisper | Noisy rural speech recognition in Indian regional dialects |
| **Indic Translation** | Bhashini / IndicTrans pipeline | Multilingual translation across Marathi, Hindi, Tamil, Telugu, and English |
| **Vision Model** | CLIP / ResNet embeddings | Dense vector extraction for motif identification and reverse image matching |
| **Security** | Werkzeug password hashing | PBKDF2:SHA256 password security, zero floor price leakage |

---

## 🎨 Editorial Design System & Color Tokens

```css
/* Custom Editorial Craft Palette Tokens */
--karigar-bg:         #F8F6F1; /* Warm Ivory Canvas */
--karigar-bgAlt:      #F0ECE3; /* Muted Sand Sidebar Surface */
--karigar-card:       #FFFFFF; /* Crisp Paper White */
--karigar-dark:       #202B29; /* Deep Forest Evergreen */
--karigar-muted:      #77766F; /* Warm Charcoal */
--karigar-terracotta: #B65E43; /* Primary Brand & Action Accent */
--karigar-gold:       #C29A55; /* Zari Gold Highlight */
--karigar-sage:       #728776; /* Heritage Verification Accent */
--karigar-border:     #E8E3D9; /* Fine Line Editorial Dividers */
--karigar-success:    #438568; /* Escrow Secured & Gate Approval */
--karigar-danger:     #B85445; /* Below-Floor Threat Alert */
```

---

## 📂 Project Directory Structure

```
KARIGAR AI/
├── .env.example                      # Template configuration environment variables
├── .gitignore                        # Git exclusion rules (protects credentials & cache)
├── README.md                         # Master documentation (this file)
├── information.txt                   # Complete raw project blueprint
├── run_app.py                        # Root launcher script
│
├── backend/                          # Backend Flask Application
│   ├── run.py                        # Server entry point (starts server on port 5000)
│   ├── config.py                     # Configuration class with URL-encoded DB connection
│   ├── requirements.txt              # Python package dependencies
│   ├── seed.py                       # High-level database seeder script
│   ├── test_api.py                   # Automated 8-test API integration suite
│   ├── validate_lifecycle.py         # End-to-end 9-step business lifecycle validation
│   │
│   ├── app/                          # Flask Application Package
│   │   ├── __init__.py               # Application factory, blueprint registration & DB setup
│   │   ├── models/                   # SQLAlchemy ORM Models
│   │   │   └── __init__.py           # User, Artisan, Product, Cost, Price, Order, etc.
│   │   ├── routes/                   # REST API Route Blueprints
│   │   │   ├── auth.py               # Authentication & session endpoints
│   │   │   ├── artisan.py            # Artisan dashboard, profile & income endpoints
│   │   │   ├── buyer.py              # Public buyer catalogue & ordering endpoints
│   │   │   ├── orders.py             # Order lifecycle management endpoints
│   │   │   ├── admin.py              # Platform governance & audit log endpoints
│   │   │   ├── agent_story.py        # Agent 1 Story & Voice endpoints
│   │   │   ├── agent_pricing.py      # Agent 2 Costing & Pricing endpoints
│   │   │   ├── agent_discovery.py    # Agent 3 Visual Discovery & RFQ endpoints
│   │   │   └── agent_negotiation.py  # Agent 4 Threat Flagging & Gate 3 endpoints
│   │   ├── agents/                   # Core AI Agent Implementations
│   │   │   ├── story_agent.py        # Voice transcription & vision motif analysis
│   │   │   ├── pricing_agent.py      # Cost breakdown & regional benchmark retrieval
│   │   │   ├── discovery_agent.py    # Visual embedding search & RFQ creation
│   │   │   └── negotiation_agent.py  # Threat detection & counteroffer generator
│   │   └── services/                 # Business Logic Services
│   │       └── approval_service.py   # Immutable audit log recording for Gates 1, 2, and 3
│   │
│   └── database/                     # Database Scripts & Raw SQL
│       ├── schema.sql                # Complete relational schema (MySQL / SQLite compatible)
│       ├── seed_data.py              # Realistic sample data seeder
│       └── db.py                     # DB connection validation helper
│
├── frontend/                         # Modern React Frontend
│   ├── package.json                  # Frontend metadata
│   ├── public/
│   │   └── index.html                # Complete Master React 18 Application (Editorial Dashboard)
│   └── src/
│       └── App.js                    # Modular component source reference
│
└── scripts/                          # Automated Tooling & Validators
    ├── validate_html.py              # Validates Babel script bracket/brace balancing
    └── validate_html_tags.py         # Validates HTML tag opening/closing hierarchy
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
* Python 3.10+
* MySQL 8.0+ running on `localhost:3306`
* Modern Web Browser (Google Chrome, Microsoft Edge, Firefox, Safari)

### 2. Environment Setup
Clone the repository and create your `.env` file:
```bash
git clone https://github.com/sanketgudade/KARIGAR-AI-AI-Powered-Business-Assistant-for-Artisans-and-Weavers.git
cd KARIGAR-AI-AI-Powered-Business-Assistant-for-Artisans-and-Weavers

cp .env.example .env
```
Ensure `.env` matches your MySQL credentials:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=Karigar_Ai
PORT=5000
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Create & Seed MySQL Database
```sql
-- In MySQL Shell:
CREATE DATABASE IF NOT EXISTS Karigar_Ai;
```
Then run the database seeder:
```bash
python backend/seed.py
```

### 5. Launch Backend Server
```bash
python backend/run.py
```
The Flask backend will start on **`http://localhost:5000`**.

### 6. Open Frontend Application
Open `frontend/public/index.html` directly in your browser:
```bash
# Windows
start frontend/public/index.html

# macOS
open frontend/public/index.html

# Linux
xdg-open frontend/public/index.html
```

---

## 🧪 Automated Verification & Test Results

The repository includes test suites verifying API integrity, business lifecycle steps, and frontend syntax:

### 1. 9-Step End-to-End Business Lifecycle Test (`backend/validate_lifecycle.py`)
```bash
python backend/validate_lifecycle.py
```
```
===========================================================================
  KARIGAR AI - 9-STEP END-TO-END LIFECYCLE VALIDATION
  'AI Recommends. Artisans Decide.'
===========================================================================

[STEP 1/9] Artisan Registers on Platform...             --> SUCCESS (Yeola cluster, Marathi)
[STEP 2/9] Artisan Uploads Craft Photos & Voice Note... --> SUCCESS (Status held at DRAFT)
[STEP 3/9] Sovereign Gate 1 Catalogue Approval...       --> SUCCESS (Cleared! DRAFT -> APPROVED)
[STEP 4/9] Sovereign Gate 2 Pricing Approval...         --> SUCCESS (Cleared! Price: ₹5000, Floor: ₹4200)
[STEP 5/9] Visual Discovery & Buyer RFQ...              --> SUCCESS (72% match, zero floor leakage)
[STEP 6/9] Buyer Negotiates Below-Floor Offer...        --> SUCCESS (Threat flagged: BELOW_FLOOR)
[STEP 7/9] Sovereign Gate 3 Counteroffer Approval...    --> SUCCESS (Cleared! Counter ₹4500 transmitted)
[STEP 8/9] Buyer Accepts Deal & Funds Escrow...         --> SUCCESS (Order confirmed: ₹225,000 in escrow)
[STEP 9/9] 6-Stage Delivery & Escrow Release...         --> SUCCESS (Delivered! Revenue: ₹273,000)

[VALIDATION COMPLETE] ALL 9 LIFECYCLE STEPS ARE 100% VERIFIED & FUNCTIONAL!
```

### 2. API Endpoint & Security Test Suite (`backend/test_api.py`)
```bash
python backend/test_api.py
```
```
[TEST 1] Testing /api/health ............................. PASS (Status: healthy)
[TEST 2] Testing /api/auth/login .......................... PASS (Logged in as: Meena Tai Jadhav)
[TEST 3] Testing /api/artisan/dashboard .................. PASS (Metrics & Price Uplift verified)
[TEST 4] Testing Agent 1: /api/agent/story/generate ...... PASS (Draft title generated, Gate 1 hold)
[TEST 5] Testing Agent 2: /api/agent/pricing/analyze ..... PASS (Total Cost: ₹2,800, Rec: ₹5,200)
[TEST 6] Testing Agent 3: /api/agent/discovery/search .... PASS (Vector similarity: 72.0%)
[TEST 7] Testing Agent 4: /api/agent/negotiation ......... PASS (Below floor flagged, Gate 3 hold)
[TEST 8] Testing Buyer Public API Confidentiality ........ PASS (Confidential floor 100% hidden)

[ALL 8 API & AGENT INTEGRITY TESTS PASSED!]
```

---

## 🏆 Summary for Hackathon Jurors

KARIGAR AI was engineered from the ground up to solve **Tech4Bharat Problem Statement 7.1** as a real-world, production-ready system. It combines deep cultural respect for India's master weavers with robust computer vision, multimodal speech processing, fair-wage cost accounting, and strict human sovereignty.

**"AI recommends. Artisans decide."**  
*Empowering Artisans. Preserving Heritage. Building Fair Markets.*
