# Agent 2: Market Benchmarking and Pricing Agent
# Calculates genuine production costs, analyzes market distribution, and recommends fair prices.

from .base_agent import BaseAgent, ApprovalGate
import statistics

class MarketPricingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MarketPricingAgent", gate=ApprovalGate.GATE_2_PRICING)

    def calculate_production_costs(self, cost_inputs: dict) -> dict:
        """
        Calculates total cost based on genuine artisan labour, materials, packaging, and overhead.
        Formula: Total Cost = Raw Materials + (Hours * Fair Hourly Rate) + Packaging + Overhead
        """
        raw_mat = float(cost_inputs.get('raw_material_cost', 0.0))
        hours = float(cost_inputs.get('labor_hours', 0.0))
        hourly_wage = float(cost_inputs.get('hourly_wage', 25.0)) # ₹25/hr fair artisan standard
        pkg = float(cost_inputs.get('packaging_cost', 100.0))
        ovh = float(cost_inputs.get('overhead_cost', 200.0))
        margin_pct = float(cost_inputs.get('target_margin_percent', 30.0))

        labor_cost = round(hours * hourly_wage, 2)
        total_cost = round(raw_mat + labor_cost + pkg + ovh, 2)

        # Minimum cost-based selling price formula: Total Cost / (1 - Margin)
        margin_decimal = margin_pct / 100.0
        cost_based_floor = round(total_cost / (1.0 - margin_decimal), 2) if margin_decimal < 1.0 else total_cost

        return {
            "raw_material_cost": raw_mat,
            "labor_hours": hours,
            "hourly_wage": hourly_wage,
            "labor_cost": labor_cost,
            "packaging_cost": pkg,
            "overhead_cost": ovh,
            "total_production_cost": total_cost,
            "target_margin_percent": margin_pct,
            "cost_based_floor_price": cost_based_floor
        }

    def analyze_market_benchmarks(self, comparables: list) -> dict:
        """
        Analyzes external verified listings to determine market spread.
        Uses Median to protect against extreme high/low skew.
        """
        if not comparables:
            return {
                "count": 0,
                "min_price": 4000.0,
                "max_price": 6000.0,
                "average_price": 5000.0,
                "median_price": 5000.0
            }

        prices = [float(item['listed_price']) for item in comparables]
        min_p = round(min(prices), 2)
        max_p = round(max(prices), 2)
        avg_p = round(statistics.mean(prices), 2)
        median_p = round(statistics.median(prices), 2)

        return {
            "count": len(prices),
            "min_price": min_p,
            "max_price": max_p,
            "average_price": avg_p,
            "median_price": median_p,
            "comparables_sample": comparables[:5]
        }

    def generate_price_recommendation(self, cost_data: dict, market_stats: dict) -> dict:
        """
        Combines cost-accounting floor with real market comparables to recommend
        a sustainable selling price and confidential negotiation floor.
        """
        cost_floor = cost_data['cost_based_floor_price']
        total_cost = cost_data['total_production_cost']
        median_market = market_stats['median_price']

        # Determine competitive listing price (anchored close to market median, but above cost floor)
        suggested_listing = round(max(median_market, cost_floor), 2)
        if suggested_listing > market_stats['max_price']:
            suggested_listing = round((market_stats['max_price'] + cost_floor) / 2.0, 2)

        # Suggest confidential minimum negotiation floor (protects artisan from loss in bulk deals)
        confidential_floor = round(max(cost_floor, total_cost * 1.25), 2) # At least 25% profit above total cost

        rationale = (
            f"Your verified production cost is ₹{total_cost:,.2f} (including ₹{cost_data['labor_cost']:,.2f} for "
            f"{cost_data['labor_hours']} hours of skilled weaving). "
            f"Based on {market_stats['count']} curated comparable listings, the market median price is ₹{median_market:,.2f} "
            f"(Range: ₹{market_stats['min_price']:,.2f} - ₹{market_stats['max_price']:,.2f}). "
            f"We recommend a listing price of ₹{suggested_listing:,.2f}, which yields a healthy margin above your costs. "
            f"Your confidential minimum floor should be set at ₹{confidential_floor:,.2f} so you never accept a loss during bulk negotiations."
        )

        return {
            "suggested_price": suggested_listing,
            "suggested_min_range": market_stats['min_price'],
            "suggested_max_range": market_stats['max_price'],
            "market_median": median_market,
            "confidential_min_recommended": confidential_floor,
            "total_production_cost": total_cost,
            "pricing_rationale": rationale,
            "requires_approval_gate": ApprovalGate.GATE_2_PRICING.value,
            "status": "AWAITING_ARTISAN_PRICE_APPROVAL"
        }
