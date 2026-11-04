import sqlite3
import os
from db import get_db_connection, init_db

def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("Database already contains data. Skipping re-seed.")
        conn.close()
        return

    # 1. Insert Users
    users = [
        ('Meena Tai Jadhav', '9823011223', 'meena.paithani@karigar.ai', 'artisan', 'mr'),
        ('Ramesh Prajapati', '9823011445', 'ramesh.pottery@karigar.ai', 'artisan', 'hi'),
        ('Ananya Sharma (FabCrafts Boutique, Pune)', '9890123456', 'procurement@fabcrafts.in', 'buyer', 'en'),
        ('Vikramaditya Rao (Heritage Hotel Chain)', '9845123999', 'vikram@heritagestays.com', 'buyer', 'en'),
        ('Admin Moderator', '9800000001', 'admin@karigar.ai', 'admin', 'en')
    ]
    cursor.executemany(
        "INSERT INTO users (name, phone, email, role, preferred_language) VALUES (?, ?, ?, ?, ?)",
        users
    )
    conn.commit()

    # 2. Insert Artisans
    artisans = [
        (1, 'Traditional Handloom Weaving (Paithani)', 'Maharashtra', 'Nashik', 'Yeola', 
         'Master weaver preserving ancient pit-loom Paithani techniques passed down across 4 generations in Yeola.', 22,
         'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80'),
        (2, 'Terracotta & Clay Craft', 'Rajasthan', 'Alwar', 'Kishangarh',
         'Traditional clay master creating water vessels, natural cooling matkas, and festival diyas.', 18,
         'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80')
    ]
    cursor.executemany(
        "INSERT INTO artisans (user_id, craft_category, state, district, village, bio, years_experience, avatar_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        artisans
    )
    conn.commit()

    # 3. Insert Market Comparables (Curated External Benchmark Dataset)
    comparables = [
        ('Traditional Saree', 'Handloom Paithani Silk Saree - Purple Border', 4500.0, 'CraftBazaar Verified Listing', 'https://example.com/item1', 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=600&q=80', 0.88, '2026-10-25'),
        ('Traditional Saree', 'Yeola Pure Silk Paithani Saree with Peacock Pallu', 5000.0, 'WeaverStory Direct Listing', 'https://example.com/item2', 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=600&q=80', 0.94, '2026-10-28'),
        ('Traditional Saree', 'Authentic Maharashtrian Paithani Silk Zari Saree', 5500.0, 'Heritage Textile Collective', 'https://example.com/item3', 'https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=600&q=80', 0.91, '2026-11-01'),
        ('Traditional Saree', 'Royal Gold Zari Peacock Weave Paithani', 6000.0, 'SareeVibes Artisan Showcase', 'https://example.com/item4', 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80', 0.89, '2026-11-02'),
        ('Traditional Saree', 'Kathpadar Silk Paithani - Festive Purple', 5200.0, 'IndiaCraft Council Store', 'https://example.com/item5', 'https://images.unsplash.com/photo-1609357605129-26f69add5d6e?auto=format&fit=crop&w=600&q=80', 0.92, '2026-11-02')
    ]
    cursor.executemany(
        "INSERT INTO market_comparables (category, product_name, listed_price, source_name, source_url, image_url, similarity_score, retrieved_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        comparables
    )
    conn.commit()

    # 4. Insert Seed Product 1 (Meena's Royal Purple Paithani Saree - active with full workflow completed)
    cursor.execute("""
        INSERT INTO products (artisan_id, title, category, description, status, lead_time_days)
        VALUES (1, 'Royal Purple Paithani Silk Saree with Peacock Pallu', 'Traditional Saree', 
        'An authentic handwoven Yeola Paithani saree woven on a traditional pit-loom using pure mulberry silk and gold zari thread. Features intricate hand-woven peacock (Mor) motifs along the pallu and traditional narali border.', 'ACTIVE_MARKET', 20)
    """)
    product_id = cursor.lastrowid

    # Product Images
    cursor.execute("""
        INSERT INTO product_images (product_id, image_url, is_primary, visual_tags)
        VALUES (?, ?, 1, 'purple, gold_zari, peacock_pallu, silk_texture, pitloom_weave')
    """, (product_id, 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80'))

    # Product Story (Agent 1 Output, Approved by Meena)
    cursor.execute("""
        INSERT INTO product_stories (product_id, original_audio_url, original_language, raw_transcript, english_translation, craft_story, artisan_approved)
        VALUES (?, 'https://assets.karigar.ai/audio/meena_paithani_rec_01.mp3', 'mr',
        'माझं नाव मीना आहे. मी येवल्यामध्ये पारंपारिक पैठणी विणते. ही कला मला माझ्या आईने आणि आजीने शिकवली. एका साडीसाठी वीस दिवसांचा अखंड वेळ लागतो. यात अस्सल रेशीम आणि मोर पल्लू आहे.',
        'My name is Meena. I weave traditional Paithani sarees in Yeola. This ancient art was taught to me by my mother and grandmother. Each saree takes twenty dedicated days on our wooden pit-loom. It features pure mulberry silk and authentic peacock motifs.',
        'Crafted with devotion by Meena Tai Jadhav from the historical weaving hub of Yeola, Maharashtra. Each thread is intertwined over 20 laborious days on traditional wooden pit-looms. The royal purple body is crowned with radiant peacock (Mor) zari craftsmanship, preserving a living legacy of Maratha royal textiles.',
        1)
    """, (product_id,))

    # Product Costs (Agent 2 Input)
    # Raw materials: ₹1,500; Labour: 40 hrs @ ₹25/hr = ₹1,000; Packaging: ₹100; Overhead: ₹200 => Total = ₹2,800
    cursor.execute("""
        INSERT INTO product_costs (product_id, raw_material_cost, labor_hours, hourly_wage, packaging_cost, overhead_cost, total_production_cost, target_margin_percent)
        VALUES (?, 1500.0, 40.0, 25.0, 100.0, 200.0, 2800.0, 30.0)
    """, (product_id,))

    # Product Pricing (Agent 2 Output, Approved by Meena)
    # Total cost = 2800, Cost floor @ 30% margin = 2800 / (1 - 0.3) = 4000.
    # Market range: 4500 - 6000. Median: 5200.
    # Approved listing: 5000. Confidential minimum floor: 4200.
    cursor.execute("""
        INSERT INTO product_prices (product_id, suggested_price, suggested_min, suggested_max, market_median, approved_listing_price, confidential_min_price, pricing_rationale, artisan_approved)
        VALUES (?, 5000.0, 4500.0, 6000.0, 5200.0, 5000.0, 4200.0, 
        'Your verified production cost is ₹2,800. With 5 comparable regional handlooms listed between ₹4,500 and ₹6,000 (median ₹5,200), a listing price of ₹5,000 preserves a healthy 44% margin while staying highly competitive. Confidential floor of ₹4,200 guarantees 33% profit even under bulk negotiation.', 1)
    """, (product_id,))

    # 5. Insert Sample Buyer Request & RFQ (FabCrafts Boutique requesting 50 sarees)
    cursor.execute("""
        INSERT INTO buyer_requests (buyer_id, product_id, quantity, custom_notes, delivery_pincode, status)
        VALUES (3, ?, 50, 'Corporate Diwali gift curation. Require identical peacock pallu weaving and gift packaging.', '411004', 'NEGOTIATING')
    """, (product_id,))
    request_id = cursor.lastrowid

    # Preliminary Quotation
    cursor.execute("""
        INSERT INTO quotations (request_id, unit_price, total_amount, lead_days, preliminary_notes, status)
        VALUES (?, 5000.0, 250000.0, 35, 'Preliminary estimate generated based on approved catalogue price of ₹5,000/saree for 50 pieces.', 'PRELIMINARY')
    """, (request_id,))
    quotation_id = cursor.lastrowid

    # Active Negotiation Round (Buyer offered ₹3,000 - BELOW FLOOR! Agent 4 triggered)
    cursor.execute("""
        INSERT INTO negotiations (quotation_id, round_number, buyer_offer_unit, ai_suggested_counter_unit, ai_rationale, ai_response_message, approved_counter_unit, artisan_status, buyer_status)
        VALUES (?, 1, 3000.0, 4500.0,
        'Buyer offer of ₹3,000 is BELOW your confidential cost floor of ₹4,200 (Total cost ₹2,800). Accepting ₹3,000 yields only ₹200/saree for 20 days of labor. Recommended counteroffer is ₹4,500, offering a 10% bulk discount while securing ₹1,700 profit per saree (₹85,000 net profit).',
        'Namaste! Thank you for considering our handcrafted Yeola Paithani sarees for your Diwali collection. Each saree requires 20 days of intricate hand-weaving with pure mulberry silk and genuine zari thread. While we cannot accommodate ₹3,000 due to high material and master-artisan labor costs, as a gesture for this bulk order of 50 units, we are pleased to offer a special artisan rate of ₹4,500 per piece.',
        4500.0, 'PENDING_ARTISAN', 'PENDING')
    """, (quotation_id,))

    # Approval Log for Gate 1 and Gate 2
    cursor.execute("""
        INSERT INTO approval_logs (artisan_id, gate_name, entity_id, action, details)
        VALUES (1, 'GATE_1_CATALOGUE', ?, 'APPROVE', 'Meena approved Marathi transcript translation and craft story text.')
    """, (product_id,))
    cursor.execute("""
        INSERT INTO approval_logs (artisan_id, gate_name, entity_id, action, details)
        VALUES (1, 'GATE_2_PRICING', ?, 'APPROVE', 'Meena approved listing price at ₹5,000 and confidential floor at ₹4,200.')
    """, (product_id,))

    # Sample Recorded Historical Order to demonstrate the Money Tracker & Price Uplift
    cursor.execute("""
        INSERT INTO orders (quotation_id, buyer_id, artisan_id, product_id, quantity, agreed_unit_price, total_amount, stage, payment_status)
        VALUES (?, 4, 1, ?, 10, 4800.0, 48000.0, 'DISPATCHED', 'ESCROW_PAID')
    """, (quotation_id, product_id))

    conn.commit()
    conn.close()
    print("KARIGAR AI database successfully seeded with Paithani Artisan, Curated Benchmark Comparables, RFQs, and Negotiation round.")

if __name__ == '__main__':
    seed_database()
