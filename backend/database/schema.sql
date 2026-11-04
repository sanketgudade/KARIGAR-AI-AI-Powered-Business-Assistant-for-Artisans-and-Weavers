-- KARIGAR AI Database Schema (MySQL & SQLite compatible)
-- Problem Statement 7.1: AI-Powered Business Assistant for Artisans and Weavers

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE,
    role VARCHAR(30) NOT NULL CHECK(role IN ('artisan', 'buyer', 'admin')),
    preferred_language VARCHAR(30) DEFAULT 'mr', -- mr: Marathi, hi: Hindi, en: English, ta: Tamil, te: Telugu
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artisans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    craft_category VARCHAR(100) NOT NULL, -- e.g. 'Paithani Saree Weaving', 'Terracotta Pottery', 'Bidriware'
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    village VARCHAR(100),
    bio TEXT,
    years_experience INTEGER DEFAULT 10,
    avatar_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artisan_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'DRAFT' CHECK(status IN ('DRAFT', 'APPROVED_LISTING', 'ACTIVE_MARKET', 'ARCHIVED')),
    lead_time_days INTEGER DEFAULT 15,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artisan_id) REFERENCES artisans(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT 1,
    visual_tags TEXT, -- JSON string or comma-separated tags e.g. 'peacock_motif, zari_border, royal_purple'
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    original_audio_url TEXT,
    original_language VARCHAR(30) DEFAULT 'mr',
    raw_transcript TEXT,
    english_translation TEXT,
    craft_story TEXT,
    artisan_approved BOOLEAN DEFAULT 0,
    approved_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_costs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL UNIQUE,
    raw_material_cost DECIMAL(10, 2) NOT NULL,
    labor_hours DECIMAL(6, 2) NOT NULL,
    hourly_wage DECIMAL(10, 2) NOT NULL,
    packaging_cost DECIMAL(10, 2) DEFAULT 0.0,
    overhead_cost DECIMAL(10, 2) DEFAULT 0.0,
    total_production_cost DECIMAL(10, 2) NOT NULL,
    target_margin_percent DECIMAL(5, 2) DEFAULT 30.0,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS market_comparables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    listed_price DECIMAL(10, 2) NOT NULL,
    source_name VARCHAR(100) NOT NULL,
    source_url TEXT,
    image_url TEXT,
    similarity_score DECIMAL(5, 2) DEFAULT 0.85,
    retrieved_date VARCHAR(20) DEFAULT '2026-11-01'
);

CREATE TABLE IF NOT EXISTS product_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL UNIQUE,
    suggested_price DECIMAL(10, 2) NOT NULL,
    suggested_min DECIMAL(10, 2) NOT NULL,
    suggested_max DECIMAL(10, 2) NOT NULL,
    market_median DECIMAL(10, 2),
    approved_listing_price DECIMAL(10, 2),
    confidential_min_price DECIMAL(10, 2), -- PROTECTED: NEVER RETURNED TO BUYERS
    pricing_rationale TEXT,
    artisan_approved BOOLEAN DEFAULT 0,
    approved_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS buyer_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    custom_notes TEXT,
    delivery_pincode VARCHAR(15),
    status VARCHAR(50) DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'QUOTED', 'NEGOTIATING', 'ORDERED', 'CANCELLED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS quotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    lead_days INTEGER NOT NULL,
    preliminary_notes TEXT,
    status VARCHAR(50) DEFAULT 'PRELIMINARY' CHECK(status IN ('PRELIMINARY', 'CONFIRMED_BY_ARTISAN', 'ACCEPTED_BY_BUYER', 'REJECTED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES buyer_requests(id)
);

CREATE TABLE IF NOT EXISTS negotiations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_id INTEGER NOT NULL,
    round_number INTEGER DEFAULT 1,
    buyer_offer_unit DECIMAL(10, 2) NOT NULL,
    ai_suggested_counter_unit DECIMAL(10, 2),
    ai_rationale TEXT,
    ai_response_message TEXT,
    approved_counter_unit DECIMAL(10, 2),
    artisan_status VARCHAR(50) DEFAULT 'PENDING_ARTISAN' CHECK(artisan_status IN ('PENDING_ARTISAN', 'APPROVED', 'MODIFIED', 'REJECTED')),
    buyer_status VARCHAR(50) DEFAULT 'PENDING' CHECK(buyer_status IN ('PENDING', 'ACCEPTED', 'REJECTED', 'COUNTERED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    artisan_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    agreed_unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    stage VARCHAR(50) DEFAULT 'PRODUCTION_QUEUED' CHECK(stage IN ('PRODUCTION_QUEUED', 'IN_PROGRESS', 'QUALITY_CHECK', 'DISPATCHED', 'DELIVERED')),
    payment_status VARCHAR(50) DEFAULT 'PENDING' CHECK(payment_status IN ('PENDING', 'ESCROW_PAID', 'RELEASED_TO_ARTISAN')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (artisan_id) REFERENCES artisans(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS approval_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artisan_id INTEGER NOT NULL,
    gate_name VARCHAR(50) NOT NULL, -- 'GATE_1_CATALOGUE', 'GATE_2_PRICING', 'GATE_3_NEGOTIATION'
    entity_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'APPROVE', 'EDIT', 'REJECT'
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
