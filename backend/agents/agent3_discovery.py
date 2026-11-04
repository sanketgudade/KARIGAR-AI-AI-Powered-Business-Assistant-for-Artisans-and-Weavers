# Agent 3: Buyer Product Discovery and Quotation Agent
# Powers reverse image visual discovery and preliminary bulk quotation estimation.

import math

class BuyerDiscoveryAndQuotationAgent:
    def __init__(self):
        self.name = "BuyerDiscoveryAndQuotationAgent"

    def match_products_by_image(self, uploaded_image_meta: dict, catalogue_products: list) -> list:
        """
        Calculates similarity between buyer's uploaded reference image and active artisan catalogue.
        Uses visual tags and attribute intersection to simulate CLIP/FAISS vector embeddings.
        """
        query_tags = set(uploaded_image_meta.get('tags', ['purple', 'paithani', 'saree', 'peacock']))
        results = []

        for prod in catalogue_products:
            prod_tags = set([t.strip().lower() for t in prod.get('visual_tags', '').split(',') if t.strip()])
            if not prod_tags:
                prod_tags = {'saree', 'handloom', 'traditional'}
            
            # Jaccard + attribute overlap baseline
            intersection = query_tags.intersection(prod_tags)
            union = query_tags.union(prod_tags)
            base_score = len(intersection) / len(union) if union else 0.5
            
            # Boost score for high-value craft markers
            similarity_pct = round(min(0.96, max(0.70, base_score + 0.35)), 2)

            results.append({
                "product_id": prod['id'],
                "title": prod['title'],
                "category": prod['category'],
                "artisan_name": prod.get('artisan_name', 'Artisan Partner'),
                "artisan_village": prod.get('village', 'Craft Hub'),
                "artisan_state": prod.get('state', 'India'),
                "approved_price": prod.get('approved_listing_price', 5000.0),
                "image_url": prod.get('image_url', ''),
                "similarity_score": similarity_pct,
                "lead_time_days": prod.get('lead_time_days', 20)
            })

        # Rank by highest similarity score
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results

    def generate_preliminary_quotation(self, product: dict, quantity: int, delivery_pincode: str = None) -> dict:
        """
        Generates initial transparent quotation for buyer review before artisan validation.
        Formula: Quotation = Quantity * Approved Unit Price (with tiered volume transparency)
        """
        unit_price = float(product.get('approved_listing_price', 5000.0))
        qty = max(1, int(quantity))
        
        # Transparent bulk rate tier calculation (informational for buyer)
        suggested_bulk_discount_pct = 0.0
        if qty >= 50:
            suggested_bulk_discount_pct = 10.0
        elif qty >= 20:
            suggested_bulk_discount_pct = 5.0

        estimated_unit_price = round(unit_price * (1.0 - suggested_bulk_discount_pct / 100.0), 2)
        total_estimate = round(qty * estimated_unit_price, 2)

        # Production lead time estimation: base lead time + scale factor for pit looms
        base_days = int(product.get('lead_time_days', 20))
        estimated_production_days = base_days + math.ceil(qty / 5) # ~5 pieces per sub-cluster batch

        return {
            "product_id": product['id'],
            "product_title": product['title'],
            "artisan_name": product.get('artisan_name', 'Master Weaver'),
            "quantity": qty,
            "catalogue_unit_price": unit_price,
            "estimated_unit_price": estimated_unit_price,
            "estimated_total_amount": total_estimate,
            "applied_tier_discount_percent": suggested_bulk_discount_pct,
            "estimated_lead_days": estimated_production_days,
            "delivery_pincode": delivery_pincode,
            "quotation_status": "PRELIMINARY",
            "terms_disclaimer": "Preliminary estimate. Requires artisan validation of loom capacity and custom requirements."
        }
