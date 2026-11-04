# Agent 3: Buyer Product Discovery and Quotation Agent
# Powers reverse image visual similarity search and preliminary wholesale quotation calculations.

import math

class BuyerDiscoveryAndQuotationAgent:
    def __init__(self):
        pass

    def search_similar_products(self, query_meta: dict, catalogue_products: list) -> list:
        """
        Calculates similarity between buyer's uploaded reference image/tags and active catalogue.
        Simulates CLIP/FAISS embedding retrieval with fallback attribute matching.
        """
        query_tags = set(query_meta.get('tags', ['purple', 'paithani', 'saree', 'peacock']))
        category = query_meta.get('category', '').lower()

        results = []
        for prod in catalogue_products:
            prod_tags_str = prod.get('visual_tags', '') or prod.get('description', '')
            prod_tags = set([t.strip().lower() for t in prod_tags_str.replace(',', ' ').split() if t.strip()])
            
            # Intersection score
            overlap = len(query_tags.intersection(prod_tags))
            total = len(query_tags.union(prod_tags)) if query_tags.union(prod_tags) else 1
            base_score = overlap / total
            
            # Similarity scaled between 0.75 and 0.96 for relevant items
            similarity = round(min(0.96, max(0.72, base_score + 0.40)), 2)

            results.append({
                'product_id': prod['product_id'],
                'title': prod['title'],
                'category': prod['category'],
                'artisan_name': prod.get('artisan_name', 'Master Artisan'),
                'artisan_location': prod.get('artisan_location', 'Maharashtra, India'),
                'approved_price': prod.get('approved_price', 5000.0),
                'image_url': prod.get('image_url', ''),
                'similarity_score': similarity,
                'production_time': prod.get('production_time', 20),
                'story_snippet': prod.get('story', {}).get('approved_story', '')[:160] + '...' if prod.get('story') else ''
            })

        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results

    def generate_preliminary_quotation(self, product: dict, quantity: int, delivery_location: str = None) -> dict:
        """
        Calculates preliminary bulk quote with volume tier transparency.
        Unit Price = Approved Catalogue Price
        Preliminary Total = Quantity * Unit Price * (1 - Tier Discount)
        """
        unit_price = float(product.get('approved_price', 5000.0))
        qty = max(1, int(quantity))

        # Volume tier guidelines
        discount_pct = 0.0
        if qty >= 50:
            discount_pct = 10.0
        elif qty >= 20:
            discount_pct = 5.0

        estimated_unit_price = round(unit_price * (1.0 - (discount_pct / 100.0)), 2)
        total_estimate = round(qty * estimated_unit_price, 2)

        # Lead time calculation
        base_days = int(product.get('production_time', 20))
        estimated_days = base_days + math.ceil(qty / 5)

        return {
            'product_id': product['product_id'],
            'product_title': product['title'],
            'artisan_name': product.get('artisan_name', 'Master Artisan'),
            'quantity': qty,
            'catalogue_unit_price': unit_price,
            'estimated_unit_price': estimated_unit_price,
            'estimated_total_amount': total_estimate,
            'volume_discount_pct': discount_pct,
            'estimated_lead_days': estimated_days,
            'delivery_location': delivery_location,
            'status': 'PRELIMINARY',
            'disclaimer': 'Preliminary estimate. Final amount and delivery schedule subject to artisan loom confirmation.'
        }
