# KARIGAR AI - Flask Backend Server
# GAVS / Tech4Bharat Hackathon 2026 - Problem Statement 7.1

import os
import sys
import json
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add current dir to sys.path
sys.path.append(os.path.dirname(__file__))

from database.db import get_db_connection, init_db
from database.seed_data import seed_database

from agents.agent1_cataloguing import StoryAndCataloguingAgent
from agents.agent2_pricing import MarketPricingAgent
from agents.agent3_discovery import BuyerDiscoveryAndQuotationAgent
from agents.agent4_negotiation import AINegotiationAgent

app = Flask(__name__)
CORS(app)

# Initialize and seed database if necessary
try:
    seed_database()
except Exception as e:
    print("Database initialization warning:", e)

# Instantiate Agents
agent1 = StoryAndCataloguingAgent()
agent2 = MarketPricingAgent()
agent3 = BuyerDiscoveryAndQuotationAgent()
agent4 = AINegotiationAgent()

# Helper serializer
def dict_from_row(row):
    return dict(row) if row else None

# ==========================================
# 1. AUTH & PROFILE APIS
# ==========================================
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    phone = data.get('phone', '9823011223') # Default to Meena Tai
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_dict = dict_from_row(user)
    artisan = conn.execute("SELECT * FROM artisans WHERE user_id = ?", (user['id'],)).fetchone()
    conn.close()

    return jsonify({
        "user": user_dict,
        "artisan": dict_from_row(artisan) if artisan else None
    })

@app.route('/api/artisan/profile', methods=['GET'])
def get_artisan_profile():
    conn = get_db_connection()
    artisan_row = conn.execute("""
        SELECT a.*, u.name, u.phone, u.email, u.preferred_language 
        FROM artisans a 
        JOIN users u ON a.user_id = u.id 
        LIMIT 1
    """).fetchone()
    conn.close()
    return jsonify(dict_from_row(artisan_row))

# ==========================================
# 2. AGENT 1: STORY & CATALOGUING APIS (GATE 1)
# ==========================================
@app.route('/api/products/generate-listing', methods=['POST'])
def generate_listing():
    """
    Agent 1 takes voice transcript + uploaded image details and synthesizes listing & craft story.
    Returns draft for Gate 1 Approval.
    """
    data = request.json or {}
    audio_data = {
        'raw_text': data.get('voice_transcript', ''),
        'translated_text': data.get('translated_text', '')
    }
    language = data.get('language', 'mr')
    image_urls = data.get('image_urls', [
        'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80'
    ])
    
    conn = get_db_connection()
    artisan = conn.execute("""
        SELECT a.*, u.name FROM artisans a JOIN users u ON a.user_id = u.id LIMIT 1
    """).fetchone()
    conn.close()

    voice_result = agent1.process_voice_input(audio_data, language=language)
    vision_result = agent1.analyze_product_images(image_urls)
    listing_draft = agent1.synthesize_listing_draft(dict_from_row(artisan), voice_result, vision_result)

    return jsonify({
        "voice_result": voice_result,
        "vision_result": vision_result,
        "listing_draft": listing_draft
    })

@app.route('/api/products/approve-listing', methods=['POST'])
def approve_listing():
    """
    APPROVAL GATE 1: Artisan explicitly approves or modifies the drafted listing.
    Transitions status: DRAFT -> APPROVED_LISTING.
    """
    data = request.json or {}
    title = data.get('title')
    category = data.get('category', 'Traditional Saree')
    description = data.get('description')
    craft_story = data.get('craft_story')
    raw_transcript = data.get('raw_transcript', '')
    english_translation = data.get('english_translation', '')
    language = data.get('language', 'mr')
    image_url = data.get('image_url', 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80')
    lead_time_days = data.get('lead_time_days', 20)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (artisan_id, title, category, description, status, lead_time_days)
        VALUES (1, ?, ?, ?, 'APPROVED_LISTING', ?)
    """, (title, category, description, lead_time_days))
    product_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO product_images (product_id, image_url, is_primary, visual_tags)
        VALUES (?, ?, 1, 'purple, gold_zari, peacock_pallu, silk_texture')
    """, (product_id, image_url))

    cursor.execute("""
        INSERT INTO product_stories (product_id, original_language, raw_transcript, english_translation, craft_story, artisan_approved, approved_at)
        VALUES (?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP)
    """, (product_id, language, raw_transcript, english_translation, craft_story))

    # Log Gate 1 event
    agent1.log_gate_event(conn, 1, product_id, 'APPROVE', 'Artisan approved product title, craft story, and technical description.')

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "product_id": product_id,
        "status": "APPROVED_LISTING",
        "message": "Gate 1 Cleared: Listing approved by artisan. Ready for Cost & Market Benchmarking."
    })

# ==========================================
# 3. AGENT 2: MARKET BENCHMARKING & PRICING APIS (GATE 2)
# ==========================================
@app.route('/api/pricing/comparables', methods=['GET'])
def get_market_comparables():
    category = request.args.get('category', 'Traditional Saree')
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM market_comparables WHERE category = ?", (category,)).fetchall()
    conn.close()
    
    comparables = [dict_from_row(r) for r in rows]
    market_stats = agent2.analyze_market_benchmarks(comparables)
    return jsonify({
        "comparables": comparables,
        "market_stats": market_stats
    })

@app.route('/api/pricing/recommend', methods=['POST'])
def recommend_price():
    """
    Agent 2 computes production costs, assesses market comparables, and recommends pricing package.
    """
    data = request.json or {}
    cost_data = agent2.calculate_production_costs(data)

    conn = get_db_connection()
    category = data.get('category', 'Traditional Saree')
    rows = conn.execute("SELECT * FROM market_comparables WHERE category = ?", (category,)).fetchall()
    conn.close()

    comparables = [dict_from_row(r) for r in rows]
    market_stats = agent2.analyze_market_benchmarks(comparables)
    recommendation = agent2.generate_price_recommendation(cost_data, market_stats)

    return jsonify({
        "cost_breakdown": cost_data,
        "market_stats": market_stats,
        "recommendation": recommendation
    })

@app.route('/api/pricing/approve', methods=['POST'])
def approve_price():
    """
    APPROVAL GATE 2: Artisan fixes the approved listing price and confidential minimum floor.
    Transitions status: APPROVED_LISTING -> ACTIVE_MARKET.
    """
    data = request.json or {}
    product_id = data.get('product_id', 1)
    approved_price = float(data.get('approved_listing_price', 5000.0))
    confidential_min = float(data.get('confidential_min_price', 4200.0))
    suggested_price = float(data.get('suggested_price', 5000.0))
    suggested_min = float(data.get('suggested_min', 4500.0))
    suggested_max = float(data.get('suggested_max', 6000.0))
    market_median = float(data.get('market_median', 5200.0))
    rationale = data.get('pricing_rationale', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Save costs if provided
    cost_data = data.get('cost_breakdown')
    if cost_data:
        cursor.execute("""
            INSERT OR REPLACE INTO product_costs 
            (product_id, raw_material_cost, labor_hours, hourly_wage, packaging_cost, overhead_cost, total_production_cost, target_margin_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (product_id, cost_data['raw_material_cost'], cost_data['labor_hours'], cost_data['hourly_wage'],
              cost_data['packaging_cost'], cost_data['overhead_cost'], cost_data['total_production_cost'], cost_data['target_margin_percent']))

    cursor.execute("""
        INSERT OR REPLACE INTO product_prices 
        (product_id, suggested_price, suggested_min, suggested_max, market_median, approved_listing_price, confidential_min_price, pricing_rationale, artisan_approved, approved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP)
    """, (product_id, suggested_price, suggested_min, suggested_max, market_median, approved_price, confidential_min, rationale))

    # Activate product for public discovery
    cursor.execute("UPDATE products SET status = 'ACTIVE_MARKET' WHERE id = ?", (product_id,))

    # Log Gate 2 event
    agent2.log_gate_event(conn, 1, product_id, 'APPROVE', f"Artisan approved public listing price ₹{approved_price:,.2f} and confidential floor ₹{confidential_min:,.2f}.")

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "product_id": product_id,
        "status": "ACTIVE_MARKET",
        "message": "Gate 2 Cleared: Price approved and product is now live in marketplace!"
    })

# ==========================================
# 4. AGENT 3: BUYER DISCOVERY & QUOTATION APIS
# ==========================================
@app.route('/api/buyer/search-image', methods=['POST'])
def search_by_image():
    """
    Agent 3 visual similarity search against active artisan catalogue.
    """
    data = request.json or {}
    image_meta = {
        'tags': data.get('tags', ['purple', 'paithani', 'peacock', 'saree', 'gold_zari'])
    }
    
    conn = get_db_connection()
    query = """
        SELECT p.id, p.title, p.category, p.description, p.lead_time_days,
               img.image_url, img.visual_tags,
               pr.approved_listing_price,
               a.village, a.state, u.name as artisan_name
        FROM products p
        LEFT JOIN product_images img ON p.id = img.product_id AND img.is_primary = 1
        LEFT JOIN product_prices pr ON p.id = pr.product_id
        JOIN artisans a ON p.artisan_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE p.status = 'ACTIVE_MARKET'
    """
    rows = conn.execute(query).fetchall()
    conn.close()

    catalogue_products = [dict_from_row(r) for r in rows]
    matches = agent3.match_products_by_image(image_meta, catalogue_products)

    return jsonify({
        "query_attributes": image_meta['tags'],
        "matched_products": matches
    })

@app.route('/api/buyer/products', methods=['GET'])
def get_buyer_catalogue():
    """
    Public catalogue. STRICT SECURITY: Never returns confidential_min_price or internal cost breakdown!
    """
    conn = get_db_connection()
    query = """
        SELECT p.id, p.title, p.category, p.description, p.lead_time_days,
               img.image_url,
               pr.approved_listing_price,
               s.craft_story,
               a.village, a.state, a.years_experience, u.name as artisan_name
        FROM products p
        LEFT JOIN product_images img ON p.id = img.product_id AND img.is_primary = 1
        LEFT JOIN product_prices pr ON p.id = pr.product_id
        LEFT JOIN product_stories s ON p.id = s.product_id
        JOIN artisans a ON p.artisan_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE p.status = 'ACTIVE_MARKET'
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict_from_row(r) for r in rows])

@app.route('/api/buyer/request-quotation', methods=['POST'])
def request_quotation():
    """
    Buyer submits bulk/single order RFQ. Agent 3 generates preliminary quotation.
    """
    data = request.json or {}
    product_id = data.get('product_id', 1)
    quantity = int(data.get('quantity', 50))
    buyer_id = data.get('buyer_id', 3)
    custom_notes = data.get('custom_notes', 'Diwali bulk requirements')
    delivery_pincode = data.get('delivery_pincode', '411004')

    conn = get_db_connection()
    cursor = conn.cursor()

    product_row = conn.execute("""
        SELECT p.*, pr.approved_listing_price, u.name as artisan_name
        FROM products p
        JOIN product_prices pr ON p.id = pr.product_id
        JOIN artisans a ON p.artisan_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE p.id = ?
    """, (product_id,)).fetchone()

    if not product_row:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    product_dict = dict_from_row(product_row)
    preliminary_quote = agent3.generate_preliminary_quotation(product_dict, quantity, delivery_pincode)

    cursor.execute("""
        INSERT INTO buyer_requests (buyer_id, product_id, quantity, custom_notes, delivery_pincode, status)
        VALUES (?, ?, ?, ?, ?, 'QUOTED')
    """, (buyer_id, product_id, quantity, custom_notes, delivery_pincode))
    request_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO quotations (request_id, unit_price, total_amount, lead_days, preliminary_notes, status)
        VALUES (?, ?, ?, ?, ?, 'PRELIMINARY')
    """, (request_id, preliminary_quote['estimated_unit_price'], preliminary_quote['estimated_total_amount'],
          preliminary_quote['estimated_lead_days'], preliminary_quote['terms_disclaimer']))
    quotation_id = cursor.lastrowid

    conn.commit()
    conn.close()

    preliminary_quote['request_id'] = request_id
    preliminary_quote['quotation_id'] = quotation_id

    return jsonify(preliminary_quote)

# ==========================================
# 5. AGENT 4: AI NEGOTIATION APIS (GATE 3)
# ==========================================
@app.route('/api/negotiation/submit-offer', methods=['POST'])
def submit_buyer_offer():
    """
    Buyer makes a counteroffer on a quotation (e.g. ₹3,000 for 50 sarees).
    Agent 4 analyzes it against confidential minimum floor and prepares draft counter.
    STRICT: AI never commits autonomously!
    """
    data = request.json or {}
    quotation_id = data.get('quotation_id', 1)
    buyer_offer_unit = float(data.get('buyer_offer_unit', 3000.0))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve quotation and product details including confidential floor
    query = """
        SELECT q.*, r.quantity, r.buyer_id, p.id as product_id, p.title,
               pr.approved_listing_price, pr.confidential_min_price,
               c.total_production_cost,
               u.name as artisan_name, a.craft_category, a.village
        FROM quotations q
        JOIN buyer_requests r ON q.request_id = r.id
        JOIN products p ON r.product_id = p.id
        JOIN product_prices pr ON p.id = pr.product_id
        JOIN product_costs c ON p.id = c.product_id
        JOIN artisans a ON p.artisan_id = a.id
        JOIN users u ON a.user_id = u.id
        WHERE q.id = ?
    """
    deal_info = conn.execute(query, (quotation_id,)).fetchone()
    if not deal_info:
        conn.close()
        return jsonify({"error": "Quotation details not found"}), 404

    deal_dict = dict_from_row(deal_info)
    offer_data = {
        'buyer_offer_unit': buyer_offer_unit,
        'quantity': deal_dict['quantity']
    }
    product_commercials = {
        'approved_listing_price': deal_dict['approved_listing_price'],
        'confidential_min_price': deal_dict['confidential_min_price'],
        'total_production_cost': deal_dict['total_production_cost']
    }
    artisan_profile = {
        'name': deal_dict['artisan_name'],
        'craft_category': deal_dict['craft_category'],
        'village': deal_dict['village']
    }

    analysis = agent4.analyze_offer(offer_data, product_commercials, artisan_profile)

    # Insert into negotiations table with artisan_status = 'PENDING_ARTISAN'
    cursor.execute("""
        INSERT INTO negotiations 
        (quotation_id, round_number, buyer_offer_unit, ai_suggested_counter_unit, ai_rationale, ai_response_message, approved_counter_unit, artisan_status, buyer_status)
        VALUES (?, 1, ?, ?, ?, ?, ?, 'PENDING_ARTISAN', 'PENDING')
    """, (quotation_id, buyer_offer_unit, analysis['ai_suggested_counter_unit'], 
          analysis['ai_rationale'], analysis['ai_drafted_response'], analysis['ai_suggested_counter_unit']))
    negotiation_id = cursor.lastrowid

    # Update quotation status
    cursor.execute("UPDATE quotations SET status = 'NEGOTIATING' WHERE id = ?", (quotation_id,))
    cursor.execute("UPDATE buyer_requests SET status = 'NEGOTIATING' WHERE id = ?", (deal_dict['request_id'],))

    conn.commit()
    conn.close()

    analysis['negotiation_id'] = negotiation_id
    return jsonify(analysis)

@app.route('/api/negotiation/details/<int:negotiation_id>', methods=['GET'])
def get_negotiation_details(negotiation_id):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT n.*, q.unit_price as original_quote_unit, r.quantity, p.title as product_title,
               pr.approved_listing_price, pr.confidential_min_price, c.total_production_cost,
               u_buyer.name as buyer_name, u_artisan.name as artisan_name
        FROM negotiations n
        JOIN quotations q ON n.quotation_id = q.id
        JOIN buyer_requests r ON q.request_id = r.id
        JOIN products p ON r.product_id = p.id
        JOIN product_prices pr ON p.id = pr.product_id
        JOIN product_costs c ON p.id = c.product_id
        JOIN users u_buyer ON r.buyer_id = u_buyer.id
        JOIN artisans a ON p.artisan_id = a.id
        JOIN users u_artisan ON a.user_id = u_artisan.id
        WHERE n.id = ?
    """, (negotiation_id,)).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Negotiation record not found"}), 404

    return jsonify(dict_from_row(row))

@app.route('/api/negotiation/artisan-action', methods=['POST'])
def artisan_negotiation_action():
    """
    APPROVAL GATE 3: Artisan reviews AI suggestion and takes sovereign action:
    - 'APPROVE': Sends AI suggested counteroffer to buyer.
    - 'MODIFY': Artisan adjusts counter price & message, then sends.
    - 'REJECT': Rejects buyer offer.
    """
    data = request.json or {}
    negotiation_id = data.get('negotiation_id', 1)
    action = data.get('action', 'APPROVE') # 'APPROVE', 'MODIFY', 'REJECT'
    approved_counter_unit = float(data.get('approved_counter_unit', 4500.0))
    custom_message = data.get('custom_message', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    if action == 'APPROVE':
        cursor.execute("""
            UPDATE negotiations 
            SET artisan_status = 'APPROVED', approved_counter_unit = ?, buyer_status = 'COUNTERED'
            WHERE id = ?
        """, (approved_counter_unit, negotiation_id))
    elif action == 'MODIFY':
        cursor.execute("""
            UPDATE negotiations 
            SET artisan_status = 'MODIFIED', approved_counter_unit = ?, ai_response_message = ?, buyer_status = 'COUNTERED'
            WHERE id = ?
        """, (approved_counter_unit, custom_message, negotiation_id))
    else:
        cursor.execute("UPDATE negotiations SET artisan_status = 'REJECTED', buyer_status = 'REJECTED' WHERE id = ?", (negotiation_id,))

    # Log Gate 3 event
    agent4.log_gate_event(conn, 1, negotiation_id, action, f"Artisan decided action {action} with counter price ₹{approved_counter_unit:,.2f}.")

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "action": action,
        "approved_counter_unit": approved_counter_unit,
        "status": "COUNTEROFFER_TRANSMITTED_TO_BUYER",
        "message": "Gate 3 Cleared: Artisan has approved the counteroffer. Buyer notified."
    })

@app.route('/api/negotiation/buyer-accept', methods=['POST'])
def buyer_accept_deal():
    """
    Buyer accepts the artisan-approved counteroffer. Order is confirmed!
    """
    data = request.json or {}
    negotiation_id = data.get('negotiation_id', 1)

    conn = get_db_connection()
    cursor = conn.cursor()

    nego = conn.execute("""
        SELECT n.*, q.id as quotation_id, r.buyer_id, r.quantity, p.id as product_id, p.artisan_id
        FROM negotiations n
        JOIN quotations q ON n.quotation_id = q.id
        JOIN buyer_requests r ON q.request_id = r.id
        JOIN products p ON r.product_id = p.id
        WHERE n.id = ?
    """, (negotiation_id,)).fetchone()

    if not nego:
        conn.close()
        return jsonify({"error": "Negotiation not found"}), 404

    deal = dict_from_row(nego)
    final_unit_price = deal['approved_counter_unit']
    total_amount = final_unit_price * deal['quantity']

    # Update negotiation & quotation
    cursor.execute("UPDATE negotiations SET buyer_status = 'ACCEPTED' WHERE id = ?", (negotiation_id,))
    cursor.execute("UPDATE quotations SET status = 'ACCEPTED_BY_BUYER', final_amount = ? WHERE id = ?", (total_amount, deal['quotation_id']))
    cursor.execute("UPDATE buyer_requests SET status = 'ORDERED' WHERE id = (SELECT request_id FROM quotations WHERE id = ?)", (deal['quotation_id'],))

    # Create confirmed Order
    cursor.execute("""
        INSERT INTO orders (quotation_id, buyer_id, artisan_id, product_id, quantity, agreed_unit_price, total_amount, stage, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'PRODUCTION_QUEUED', 'ESCROW_PAID')
    """, (deal['quotation_id'], deal['buyer_id'], deal['artisan_id'], deal['product_id'], deal['quantity'], final_unit_price, total_amount))
    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "order_id": order_id,
        "final_unit_price": final_unit_price,
        "total_amount": total_amount,
        "stage": "PRODUCTION_QUEUED",
        "message": "Commercial deal confirmed! Escrow advance registered. Order enters production lifecycle."
    })

# ==========================================
# 6. MONEY TRACKER & ARTISAN DASHBOARD
# ==========================================
@app.route('/api/artisan/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    conn = get_db_connection()
    
    # Orders aggregate
    orders_res = conn.execute("""
        SELECT COUNT(*) as total_orders,
               COALESCE(SUM(total_amount), 0) as total_revenue,
               COALESCE(AVG(agreed_unit_price), 0) as avg_selling_price
        FROM orders
        WHERE artisan_id = 1
    """).fetchone()

    # Active enquiries & negotiations
    pending_nego = conn.execute("""
        SELECT COUNT(*) as pending_negotiations 
        FROM negotiations 
        WHERE artisan_status = 'PENDING_ARTISAN'
    """).fetchone()

    # Historical price comparison benchmark
    # Traditional middleman average for Yeola Paithani was ~₹3,000.
    # Current direct platform average is ~₹4,800.
    avg_price = float(orders_res['avg_selling_price']) if orders_res['avg_selling_price'] else 4800.0
    traditional_middleman_price = 3000.0
    realized_price_uplift = round(avg_price - traditional_middleman_price, 2)

    # Active products list
    products = conn.execute("""
        SELECT p.*, pr.approved_listing_price, pr.confidential_min_price, img.image_url
        FROM products p
        LEFT JOIN product_prices pr ON p.id = pr.product_id
        LEFT JOIN product_images img ON p.id = img.product_id AND img.is_primary = 1
        WHERE p.artisan_id = 1
    """).fetchall()

    # Recent orders
    recent_orders = conn.execute("""
        SELECT o.*, p.title as product_title, u.name as buyer_name
        FROM orders o
        JOIN products p ON o.product_id = p.id
        JOIN users u ON o.buyer_id = u.id
        WHERE o.artisan_id = 1
        ORDER BY o.id DESC LIMIT 5
    """).fetchall()

    # Approval Logs (Verification audit trail)
    approval_logs = conn.execute("""
        SELECT * FROM approval_logs WHERE artisan_id = 1 ORDER BY id DESC LIMIT 10
    """).fetchall()

    conn.close()

    return jsonify({
        "summary": {
            "total_orders": orders_res['total_orders'],
            "total_revenue": orders_res['total_revenue'],
            "average_selling_price": round(avg_price, 2),
            "pending_negotiations": pending_nego['pending_negotiations'],
            "traditional_middleman_price": traditional_middleman_price,
            "realized_price_uplift": realized_price_uplift,
            "realized_price_uplift_percent": round((realized_price_uplift / traditional_middleman_price) * 100, 1)
        },
        "products": [dict_from_row(p) for p in products],
        "recent_orders": [dict_from_row(o) for o in recent_orders],
        "approval_logs": [dict_from_row(l) for l in approval_logs]
    })

@app.route('/api/orders/update-stage', methods=['POST'])
def update_order_stage():
    data = request.json or {}
    order_id = data.get('order_id')
    new_stage = data.get('stage') # 'IN_PROGRESS', 'QUALITY_CHECK', 'DISPATCHED', 'DELIVERED'

    conn = get_db_connection()
    conn.execute("UPDATE orders SET stage = ? WHERE id = ?", (new_stage, order_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "order_id": order_id, "stage": new_stage})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting KARIGAR AI Backend Server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
