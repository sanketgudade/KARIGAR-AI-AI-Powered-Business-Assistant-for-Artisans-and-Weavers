"""
KARIGAR AI - Seed Data Script
Problem Statement 7.1: GAVS / Tech4Bharat Hackathon 2026
Populates realistic artisan profiles, products, curated market comparables, RFQs, negotiations, and orders.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models import (
    db, User, Artisan, Product, ProductImage, ProductStory,
    ProductCost, ProductPrice, MarketComparable, BuyerRequest,
    Quotation, Negotiation, Approval, Order, Payment
)

def seed_database():
    app = create_app()
    with app.app_context():
        # Create all tables in MySQL
        db.create_all()

        if User.query.count() > 0:
            print("Database already contains records. Clearing and reseeding clean hackathon demo data...")
            # Delete in reverse foreign key order
            Payment.query.delete()
            Order.query.delete()
            Approval.query.delete()
            Negotiation.query.delete()
            Quotation.query.delete()
            BuyerRequest.query.delete()
            ProductPrice.query.delete()
            MarketComparable.query.delete()
            ProductCost.query.delete()
            ProductStory.query.delete()
            ProductImage.query.delete()
            Product.query.delete()
            Artisan.query.delete()
            User.query.delete()
            db.session.commit()

        print("[1/5] Seeding Users and Master Artisans...")
        # 1. Users
        u_meena = User(name="Meena Tai Jadhav", phone="9823011223", email="meena.paithani@karigar.ai", role="artisan", preferred_language="mr")
        u_meena.set_password("password123")
        
        u_lakshmi = User(name="Lakshmi Ammal", phone="9840123456", email="lakshmi.kanchi@karigar.ai", role="artisan", preferred_language="ta")
        u_lakshmi.set_password("password123")
        
        u_ramesh = User(name="Ramesh Prajapati", phone="9829012345", email="ramesh.pottery@karigar.ai", role="artisan", preferred_language="hi")
        u_ramesh.set_password("password123")

        u_farida = User(name="Farida Khatun", phone="9879012345", email="farida.embroidery@karigar.ai", role="artisan", preferred_language="hi")
        u_farida.set_password("password123")

        u_buyer = User(name="Ananya Sharma (FabCrafts Boutique, Pune)", phone="9890123456", email="procurement@fabcrafts.in", role="buyer", preferred_language="en")
        u_buyer.set_password("password123")

        u_admin = User(name="Admin Moderator", phone="9800000001", email="admin@karigar.ai", role="admin", preferred_language="en")
        u_admin.set_password("password123")

        db.session.add_all([u_meena, u_lakshmi, u_ramesh, u_farida, u_buyer, u_admin])
        db.session.flush()

        # 2. Artisans
        a_meena = Artisan(
            user_id=u_meena.user_id,
            location="Yeola, Nashik, Maharashtra",
            state="Maharashtra",
            district="Nashik",
            village="Yeola",
            craft_category="Paithani Saree Weaving",
            biography="4th-generation master pit-loom weaver preserving traditional Yeola Paithani motifs including peacock pallu and narali borders.",
            years_experience=22,
            avatar_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80"
        )
        a_lakshmi = Artisan(
            user_id=u_lakshmi.user_id,
            location="Kanchipuram, Tamil Nadu",
            state="Tamil Nadu",
            district="Kanchipuram",
            village="Kanchipuram",
            craft_category="Kanchipuram Silk Weaving",
            biography="Master weaver specializing in Korvai technique pure silk sarees with heavy zari borders.",
            years_experience=26,
            avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80"
        )
        a_ramesh = Artisan(
            user_id=u_ramesh.user_id,
            location="Kot Jewar, Jaipur, Rajasthan",
            state="Rajasthan",
            district="Jaipur",
            village="Kot Jewar",
            craft_category="Jaipur Blue Pottery",
            biography="Artisan crafting traditional Egyptian faience and quartz-based glazed pottery using oxide colors.",
            years_experience=18,
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80"
        )
        a_farida = Artisan(
            user_id=u_farida.user_id,
            location="Bhujodi, Kutch, Gujarat",
            state="Gujarat",
            district="Kutch",
            village="Bhujodi",
            craft_category="Kutch Mirror & Suf Embroidery",
            biography="Master artisan preserving counted-thread geometric Suf embroidery and traditional mirror work.",
            years_experience=15,
            avatar_url="https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?auto=format&fit=crop&w=400&q=80"
        )

        db.session.add_all([a_meena, a_lakshmi, a_ramesh, a_farida])
        db.session.flush()

        print("[2/5] Seeding Curated Market Comparables Dataset (Demonstration Benchmarks)...")
        # 3. Market Comparables
        comparables = [
            MarketComparable(category="Sarees", product_name="Handloom Paithani Silk Saree - Purple Border", listed_price=4500.0, source="CraftBazaar Verified Listing", retrieval_date="2026-10-25", attributes="Purple, Zari Border", image_url="https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=600&q=80", similarity_score=0.88),
            MarketComparable(category="Sarees", product_name="Yeola Pure Silk Paithani Saree with Peacock Pallu", listed_price=5000.0, source="WeaverStory Direct Listing", retrieval_date="2026-10-28", attributes="Peacock Pallu, Gold Zari", image_url="https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=600&q=80", similarity_score=0.94),
            MarketComparable(category="Sarees", product_name="Authentic Maharashtrian Paithani Silk Zari Saree", listed_price=5500.0, source="Heritage Textile Collective", retrieval_date="2026-11-01", attributes="Narali Border, Pure Silk", image_url="https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=600&q=80", similarity_score=0.91),
            MarketComparable(category="Sarees", product_name="Royal Gold Zari Peacock Weave Paithani", listed_price=6000.0, source="SareeVibes Artisan Showcase", retrieval_date="2026-11-02", attributes="Heavy Pallu, Royal Purple", image_url="https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80", similarity_score=0.89),
            MarketComparable(category="Sarees", product_name="Kathpadar Silk Paithani - Festive Purple", listed_price=5200.0, source="IndiaCraft Council Store", retrieval_date="2026-11-02", attributes="Kathpadar, Traditional Weave", image_url="https://images.unsplash.com/photo-1609357605129-26f69add5d6e?auto=format&fit=crop&w=600&q=80", similarity_score=0.92)
        ]
        db.session.add_all(comparables)

        print("[3/5] Seeding Products, Stories, Costs, and Sovereign Approvals...")
        # 4. Product 1: Meena's Royal Purple Paithani Saree (Fully Cleared Gate 1 & Gate 2)
        p1 = Product(
            artisan_id=a_meena.artisan_id,
            title="Handcrafted Royal Purple Paithani Silk Saree with Peacock Zari Pallu",
            category="Sarees",
            description="Authentic handloom pit-loom Paithani saree in royal purple mulberry silk with intricately hand-intertwined peacock (Mor) zari motifs and traditional coconut border.",
            approved_price=5000.0,
            availability="Made to Order",
            production_time=20,
            status="ACTIVE_MARKET"
        )
        db.session.add(p1)
        db.session.flush()

        # Product Image
        img1 = ProductImage(
            product_id=p1.product_id,
            image_url="https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80",
            is_primary=True,
            visual_tags="purple, paithani, peacock_pallu, gold_zari, silk, yeola"
        )
        db.session.add(img1)

        # Product Story (Agent 1 Output, Approved by Meena)
        story1 = ProductStory(
            product_id=p1.product_id,
            original_transcript="माझं नाव मीना आहे. मी येवल्यामध्ये पारंपारिक पैठणी विणते. ही कला मला माझ्या आईने शिकवली. एका साडीसाठी वीस दिवसांचा अखंड वेळ लागतो. यात अस्सल रेशीम आणि मोर पल्लू आहे.",
            translated_text="My name is Meena. I weave traditional Paithani sarees in Yeola. This art was taught to me by my mother. Each saree takes 20 days on our wooden pit-loom. It features pure mulberry silk and authentic peacock motifs.",
            approved_story="Handcrafted with living heritage by master weaver Meena Tai Jadhav in Yeola, Maharashtra. Each thread is intertwined over 20 laborious days on traditional wooden pit-looms. The royal purple body is crowned with radiant peacock (Mor) zari craftsmanship, preserving a living legacy of Maratha royal textiles.",
            original_language="mr",
            artisan_approved=True
        )
        db.session.add(story1)

        # Product Costs (Agent 2 Input)
        # Material: 1500, Labour: 20 hrs @ 50/hr = 1000, Packaging: 200, Other: 100 => Total = 2800.
        # Cost Floor @ 30% margin = 2800 / 0.70 = 4000.
        cost1 = ProductCost(
            product_id=p1.product_id,
            material_cost=1500.0,
            labour_hours=20.0,
            labour_rate=50.0,
            packaging_cost=200.0,
            other_expenses=100.0,
            total_cost=2800.0,
            target_margin=30.0
        )
        db.session.add(cost1)

        # Product Price (Agent 2 Output, Approved by Meena)
        price1 = ProductPrice(
            product_id=p1.product_id,
            suggested_minimum=4500.0,
            suggested_maximum=6000.0,
            suggested_price=5000.0,
            market_median=5200.0,
            approved_price=5000.0,
            confidential_minimum_price=4200.0, # CONFIDENTIAL FLOOR
            pricing_rationale="Your production cost is ₹2,800. Across 5 market comparables (median ₹5,200), ₹5,000 yields a 44% gross margin while staying competitive. Confidential floor of ₹4,200 guarantees at least 33% profit during negotiations.",
            artisan_approved=True
        )
        db.session.add(price1)

        # Approval Logs for Gate 1 and Gate 2
        app1 = Approval(entity_id=p1.product_id, artisan_id=a_meena.artisan_id, approval_type="GATE_1_CATALOGUE", decision="APPROVE", comments="Approved Marathi translation & pit-loom craft story.")
        app2 = Approval(entity_id=p1.product_id, artisan_id=a_meena.artisan_id, approval_type="GATE_2_PRICING", decision="APPROVE", comments="Approved public price at ₹5,000 and confidential floor at ₹4,200.")
        db.session.add_all([app1, app2])

        # Product 2: Blue Pottery Vase by Ramesh
        p2 = Product(
            artisan_id=a_ramesh.artisan_id,
            title="Handmade Turquoise Floral Blue Pottery Urn Vase",
            category="Pottery",
            description="Traditional Jaipur blue pottery vase handcrafted with quartz, raw glaze, and Persian cobalt blue floral motifs. Completely handmade without clay.",
            approved_price=1800.0,
            availability="In Stock",
            production_time=7,
            status="ACTIVE_MARKET"
        )
        db.session.add(p2)
        db.session.flush()
        img2 = ProductImage(product_id=p2.product_id, image_url="https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80", is_primary=True, visual_tags="pottery, blue, vase, floral, jaipur")
        db.session.add(img2)

        # Product 3: Kanchipuram Silk Saree by Lakshmi
        p3 = Product(
            artisan_id=a_lakshmi.artisan_id,
            title="Temple Border Crimson Red Kanchipuram Pure Silk Saree",
            category="Sarees",
            description="Woven using heavy Mulberry silk and gold zari in the ancient Korvai technique with Mayil (peacock) and Rudraksha motifs along temple borders.",
            approved_price=8500.0,
            availability="Made to Order",
            production_time=25,
            status="ACTIVE_MARKET"
        )
        db.session.add(p3)
        db.session.flush()
        img3 = ProductImage(product_id=p3.product_id, image_url="https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80", is_primary=True, visual_tags="red, kanchipuram, silk, gold_zari, temple_border")
        db.session.add(img3)

        print("[4/5] Seeding Active Buyer RFQ, Agent 4 Negotiation Round, and Order...")
        # 5. Buyer Request from FabCrafts for 50 Paithani Sarees
        req1 = BuyerRequest(
            buyer_id=u_buyer.user_id,
            product_id=p1.product_id,
            quantity=50,
            requirements="Corporate Diwali gifting collection. Identical peacock pallu hand-weaving and customized artisan story cards required.",
            delivery_location="Pune, Maharashtra",
            status="NEGOTIATING"
        )
        db.session.add(req1)
        db.session.flush()

        # Preliminary Quotation (Approved price 5000 x 50 = 250000)
        q1 = Quotation(
            request_id=req1.request_id,
            unit_price=5000.0,
            estimated_amount=250000.0,
            lead_days=35,
            status="PRELIMINARY"
        )
        db.session.add(q1)
        db.session.flush()

        # Active Negotiation Round: Buyer offered ₹3,000 (Below Floor! Agent 4 counter @ ₹4,500)
        nego1 = Negotiation(
            quotation_id=q1.quotation_id,
            round_number=1,
            buyer_offer=3000.0,
            suggested_counteroffer=4500.0,
            approved_counteroffer=4500.0,
            ai_rationale="⚠️ Buyer offer of ₹3,000 is BELOW your confidential cost floor of ₹4,200! Total cost is ₹2,800. Accepting ₹3,000 leaves only ₹200/piece for 20 days of work. Recommended counteroffer of ₹4,500 gives buyer a 10% wholesale discount while securing ₹1,700 profit per saree (₹85,000 net profit).",
            response_message="Namaste! Thank you for considering our handcrafted Yeola Paithani sarees for your Diwali collection. Each saree requires 20 days of intricate hand-weaving with pure mulberry silk and genuine zari thread. While we cannot accommodate ₹3,000 due to high material and master-artisan labor costs, for this bulk order of 50 units, we are pleased to offer a special artisan rate of ₹4,500 per piece.",
            artisan_status="PENDING_ARTISAN", # STRICT: Gate 3 hold
            buyer_status="PENDING"
        )
        db.session.add(nego1)

        print("[5/5] Seeding Completed Historical Order for Money Tracker...")
        # 6. Completed Historical Order (10 Sarees @ ₹4,800 = ₹48,000)
        hist_req = BuyerRequest(buyer_id=u_buyer.user_id, product_id=p1.product_id, quantity=10, requirements="Boutique sample lot", delivery_location="Pune", status="ORDERED")
        db.session.add(hist_req)
        db.session.flush()

        hist_quote = Quotation(request_id=hist_req.request_id, unit_price=4800.0, estimated_amount=48000.0, final_amount=48000.0, lead_days=15, status="ACCEPTED_BY_BUYER")
        db.session.add(hist_quote)
        db.session.flush()

        hist_order = Order(
            quotation_id=hist_quote.quotation_id,
            buyer_id=u_buyer.user_id,
            artisan_id=a_meena.artisan_id,
            product_id=p1.product_id,
            quantity=10,
            unit_price=4800.0,
            total_amount=48000.0,
            order_status="DISPATCHED",
            payment_status="ESCROW_PAID"
        )
        db.session.add(hist_order)
        db.session.flush()

        hist_payment = Payment(order_id=hist_order.order_id, amount=48000.0, payment_status="ESCROW_PAID")
        db.session.add(hist_payment)

        db.session.commit()
        print("\n[SUCCESS] Seed completed successfully! Database populated with 4 artisans, products, comparables, RFQs, negotiations, and orders.")

if __name__ == '__main__':
    seed_database()
