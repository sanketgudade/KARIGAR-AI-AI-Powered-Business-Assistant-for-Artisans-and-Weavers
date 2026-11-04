# Agent 4: AI Negotiation Agent
# Analyzes buyer offers against confidential minimum floor and prepares strategic counteroffers.
# Strict Rule: AI assists, drafts, and advises; the artisan must explicitly approve before sending.

class AINegotiationAgent:
    def __init__(self):
        pass

    def evaluate_buyer_offer(self, buyer_offer: float, quantity: int, product_data: dict, artisan_data: dict) -> dict:
        """
        Threshold comparisons performed in Python.
        Never discloses confidential_minimum_price.
        """
        listing_price = float(product_data.get('approved_price', 5000.0))
        confidential_floor = float(product_data.get('confidential_minimum_price', 4200.0))
        production_cost = float(product_data.get('total_cost', 2800.0))
        craft = artisan_data.get('craft_category', 'Traditional Handloom Weaving')
        artisan_name = artisan_data.get('name', 'Artisan')
        village = artisan_data.get('village', 'Yeola')

        # Scenario 1: Favorable offer at or above listing price
        if buyer_offer >= listing_price:
            decision = "RECOMMEND_ACCEPT"
            suggested_counter = buyer_offer
            is_below_floor = False
            rationale = (
                f"The buyer has offered ₹{buyer_offer:,.2f}, which is at or above your listed price of ₹{listing_price:,.2f}. "
                f"This generates a net profit of ₹{(buyer_offer - production_cost) * quantity:,.2f} across {quantity} units."
            )
            draft_message = (
                f"Namaste! Thank you for your appreciation of our handcrafted {craft}. "
                f"We are delighted to accept your offer of ₹{buyer_offer:,.2f} per unit for {quantity} handcrafted pieces. "
                f"We will immediately reserve loom capacity in {village} to begin production."
            )

        # Scenario 2: Offer between confidential floor and listing price
        elif buyer_offer >= confidential_floor:
            decision = "VIABLE_OFFER"
            suggested_counter = round((buyer_offer + listing_price) / 2.0, 2)
            is_below_floor = False
            profit_unit = buyer_offer - production_cost
            total_profit = profit_unit * quantity
            rationale = (
                f"Buyer offer of ₹{buyer_offer:,.2f} is above your confidential floor of ₹{confidential_floor:,.2f}. "
                f"This deal guarantees ₹{profit_unit:,.2f} profit per unit (Total profit: ₹{total_profit:,.2f}). "
                f"You may accept directly, or counter at ₹{suggested_counter:,.2f} to optimize your returns."
            )
            draft_message = (
                f"Thank you for your bulk order inquiry of {quantity} pieces. While our listed rate is ₹{listing_price:,.2f}, "
                f"in consideration of your wholesale volume, we can offer a revised rate of ₹{suggested_counter:,.2f} per piece."
            )

        # Scenario 3: Predatory or loss-making offer below confidential floor
        else:
            decision = "BELOW_CONFIDENTIAL_FLOOR"
            is_below_floor = True
            # Recommend counteroffer offering reasonable 10% volume discount, strictly above floor
            suggested_counter = max(confidential_floor, round(listing_price * 0.90, 2))
            loss_margin = (buyer_offer - production_cost) * quantity
            
            rationale = (
                f"⚠️ Buyer offer of ₹{buyer_offer:,.2f} is BELOW your confidential minimum floor of ₹{confidential_floor:,.2f}! "
                f"Your true production cost is ₹{production_cost:,.2f}. Accepting ₹{buyer_offer:,.2f} would leave only ₹{buyer_offer - production_cost:,.2f}/piece "
                f"for weeks of skilled labor. "
                f"We recommend countering at ₹{suggested_counter:,.2f}, extending a 10% wholesale discount while securing "
                f"₹{(suggested_counter - production_cost) * quantity:,.2f} in total profit."
            )
            draft_message = (
                f"Namaste! Thank you for your interest in our handcrafted {craft} from {village}. "
                f"Each saree requires 20 days of intensive manual pit-loom weaving using pure mulberry silk and authentic gold zari thread. "
                f"Due to the uncompromising quality of raw materials and master artisan craftsmanship, we cannot sustain ₹{buyer_offer:,.2f}. "
                f"However, to foster a long-term partnership for your order of {quantity} units, we are pleased to extend a special artisan direct price of ₹{suggested_counter:,.2f} per piece."
            )

        return {
            'decision': decision,
            'buyer_offer': buyer_offer,
            'quantity': quantity,
            'listing_price': listing_price,
            'production_cost': production_cost,
            'is_below_floor': is_below_floor,
            'suggested_counteroffer': suggested_counter,
            'projected_profit': round((suggested_counter - production_cost) * quantity, 2),
            'ai_rationale': rationale,
            'ai_response_message': draft_message,
            'approval_gate_required': 'GATE_3_DEAL',
            'artisan_status': 'PENDING_ARTISAN',
            'notice': 'AI is an assistant. This message will NOT be sent until the artisan clicks Approve.'
        }
