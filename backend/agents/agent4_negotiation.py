# Agent 4: AI Negotiation Agent
# Analyzes buyer offers against confidential minimum floor and formulates respectful, value-articulating counteroffers.

from .base_agent import BaseAgent, ApprovalGate

class AINegotiationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AINegotiationAgent", gate=ApprovalGate.GATE_3_DEAL)

    def analyze_offer(self, offer_data: dict, product_commercials: dict, artisan_profile: dict) -> dict:
        """
        Evaluates buyer offer against confidential floor and listing price.
        Strict Rule: Never exposes confidential_min_price to the buyer.
        """
        buyer_offer = float(offer_data.get('buyer_offer_unit', 0.0))
        quantity = int(offer_data.get('quantity', 1))
        
        listing_price = float(product_commercials.get('approved_listing_price', 5000.0))
        confidential_floor = float(product_commercials.get('confidential_min_price', 4200.0))
        production_cost = float(product_commercials.get('total_production_cost', 2800.0))

        artisan_name = artisan_profile.get('name', 'Meena Tai')
        craft = artisan_profile.get('craft_category', 'Paithani Weaving')
        village = artisan_profile.get('village', 'Yeola')

        # Scenario evaluation
        if buyer_offer >= listing_price:
            decision = "ACCEPT_OFFER"
            suggested_counter = buyer_offer
            rationale = (
                f"The buyer has offered ₹{buyer_offer:,.2f}, which is at or above your listed price of ₹{listing_price:,.2f}. "
                f"This generates a net profit of ₹{(buyer_offer - production_cost) * quantity:,.2f} across {quantity} units."
            )
            response_message = (
                f"Namaste! Thank you for your generous appreciation of our authentic {craft}. "
                f"We are delighted to accept your offer of ₹{buyer_offer:,.2f} per unit for {quantity} handcrafted pieces. "
                f"We will immediately reserve loom capacity in {village} to begin production."
            )

        elif buyer_offer >= confidential_floor:
            decision = "ACCEPTABLE_WITH_OPTIONAL_COUNTER"
            # Offer is within acceptable band; suggest split or accept depending on volume
            suggested_counter = round((buyer_offer + listing_price) / 2.0, 2)
            profit_per_unit = buyer_offer - production_cost
            total_profit = profit_per_unit * quantity

            rationale = (
                f"Buyer offer of ₹{buyer_offer:,.2f} is above your confidential floor of ₹{confidential_floor:,.2f}. "
                f"This deal generates ₹{profit_per_unit:,.2f} profit per unit (Total profit: ₹{total_profit:,.2f}). "
                f"You may accept directly, or counter at ₹{suggested_counter:,.2f} to optimize earnings."
            )
            response_message = (
                f"Thank you for your bulk order enquiry of {quantity} sarees. While our listed rate is ₹{listing_price:,.2f}, "
                f"in consideration of your wholesale volume, we can offer a revised rate of ₹{suggested_counter:,.2f} per piece."
            )

        else:
            # Below confidential floor (e.g. ₹3,000 vs floor ₹4,200)
            decision = "BELOW_CONFIDENTIAL_FLOOR"
            
            # Suggest a strategic counteroffer that provides bulk value while strictly safeguarding margin
            # e.g. 10% discount from listing price = ₹4,500 (above floor ₹4,200)
            suggested_counter = max(confidential_floor, round(listing_price * 0.90, 2))
            loss_or_low_gain = (buyer_offer - production_cost) * quantity

            rationale = (
                f"⚠️ Buyer offer of ₹{buyer_offer:,.2f} is BELOW your confidential minimum floor of ₹{confidential_floor:,.2f}! "
                f"Your true cost is ₹{production_cost:,.2f}. Accepting ₹{buyer_offer:,.2f} would leave only ₹{buyer_offer - production_cost:,.2f}/piece "
                f"for 20 days of intensive labor. "
                f"We strongly recommend countering at ₹{suggested_counter:,.2f}, which offers a 10% volume discount while securing "
                f"₹{(suggested_counter - production_cost) * quantity:,.2f} total profit."
            )
            response_message = (
                f"Namaste! Thank you for considering our handcrafted {craft} from {village}. "
                f"Each saree requires 20 days of intensive manual pit-loom weaving using pure mulberry silk and authentic gold zari thread. "
                f"Due to the uncompromising quality of raw materials and master artisan craftsmanship, we cannot sustain ₹{buyer_offer:,.2f}. "
                f"However, to foster a long-term partnership for your order of {quantity} units, we are pleased to extend a special artisan direct price of ₹{suggested_counter:,.2f} per piece."
            )

        return {
            "decision": decision,
            "buyer_offer_unit": buyer_offer,
            "quantity": quantity,
            "listing_price": listing_price,
            "production_cost": production_cost,
            "is_below_floor": buyer_offer < confidential_floor,
            "ai_suggested_counter_unit": suggested_counter,
            "projected_profit_at_counter": round((suggested_counter - production_cost) * quantity, 2),
            "ai_rationale": rationale,
            "ai_drafted_response": response_message,
            "requires_approval_gate": ApprovalGate.GATE_3_DEAL.value,
            "artisan_approval_status": "PENDING_ARTISAN_CONFIRMATION",
            "enforcement_notice": "AI is an assistant. This counteroffer will NOT be transmitted to the buyer until you click 'Approve & Send'."
        }
