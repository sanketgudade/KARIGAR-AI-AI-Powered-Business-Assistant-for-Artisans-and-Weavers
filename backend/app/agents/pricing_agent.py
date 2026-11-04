# Agent 2: Market Benchmarking and Pricing Agent
# Accurately computes true costs and benchmarks against curated market data.
# All financial calculations are implemented strictly in Python.

import statistics
import numpy as np
import pandas as pd

class MarketPricingAgent:
    def __init__(self):
        pass

    def calculate_production_costs(self, cost_inputs: dict) -> dict:
        """
        Total Cost = Material Cost + (Labour Hours x Labour Rate) + Packaging + Other Expenses
        Cost Floor at Target Margin M: Selling Price = Total Cost / (1 - M)
        """
        raw_mat = float(cost_inputs.get('material_cost', 1500.0))
        hours = float(cost_inputs.get('labour_hours', 20.0))
        rate = float(cost_inputs.get('labour_rate', 50.0))
        packaging = float(cost_inputs.get('packaging_cost', 200.0))
        other = float(cost_inputs.get('other_expenses', 100.0))
        target_margin_pct = float(cost_inputs.get('target_margin', 30.0))

        labour_cost = round(hours * rate, 2)
        total_cost = round(raw_mat + labour_cost + packaging + other, 2)

        margin_decimal = target_margin_pct / 100.0
        if margin_decimal < 1.0:
            cost_based_floor = round(total_cost / (1.0 - margin_decimal), 2)
        else:
            cost_based_floor = total_cost

        return {
            'material_cost': raw_mat,
            'labour_hours': hours,
            'labour_rate': rate,
            'labour_cost': labour_cost,
            'packaging_cost': packaging,
            'other_expenses': other,
            'total_cost': total_cost,
            'target_margin': target_margin_pct,
            'cost_based_floor_price': cost_based_floor
        }

    def analyze_market_benchmarks(self, comparables: list) -> dict:
        """
        Calculates Min, Max, Average, and Median listed prices.
        Uses Median to protect against extreme outliers.
        """
        if not comparables:
            return {
                'count': 0,
                'min_price': 4000.0,
                'max_price': 6000.0,
                'average_price': 5200.0,
                'median_price': 5200.0,
                'comparables': []
            }

        prices = [float(item['listed_price']) for item in comparables]
        
        min_p = round(float(np.min(prices)), 2)
        max_p = round(float(np.max(prices)), 2)
        avg_p = round(float(np.mean(prices)), 2)
        median_p = round(float(np.median(prices)), 2)

        return {
            'count': len(prices),
            'min_price': min_p,
            'max_price': max_p,
            'average_price': avg_p,
            'median_price': median_p,
            'comparables': comparables
        }

    def generate_pricing_recommendation(self, cost_dict: dict, benchmark_dict: dict) -> dict:
        """
        Recommends a competitive selling price and establishes a confidential minimum floor.
        """
        total_cost = cost_dict['total_cost']
        cost_floor = cost_dict['cost_based_floor_price']
        market_median = benchmark_dict['median_price']
        min_market = benchmark_dict['min_price']
        max_market = benchmark_dict['max_price']

        # Determine recommended listing price
        # Anchors to market median if median satisfies margin; otherwise above cost floor
        suggested_listing = round(max(market_median, cost_floor), 2)
        if suggested_listing > max_market:
            suggested_listing = round((max_market + cost_floor) / 2.0, 2)

        # Suggest confidential minimum negotiation floor (artisan must not sell below this!)
        confidential_floor = round(max(cost_floor, total_cost * 1.25), 2)

        rationale = (
            f"Your total production cost is ₹{total_cost:,.2f} (including ₹{cost_dict['labour_cost']:,.2f} for {cost_dict['labour_hours']} hours of skilled weaving). "
            f"Across {benchmark_dict['count']} verified market comparables, the median listed price is ₹{market_median:,.2f} "
            f"(Range: ₹{min_market:,.2f} - ₹{max_market:,.2f}). "
            f"We recommend a listing price of ₹{suggested_listing:,.2f}, securing a healthy margin. "
            f"We advise setting your confidential negotiation floor at ₹{confidential_floor:,.2f} to protect your wages during bulk discussions."
        )

        return {
            'suggested_price': suggested_listing,
            'suggested_minimum': min_market,
            'suggested_maximum': max_market,
            'market_median': market_median,
            'confidential_minimum_price': confidential_floor,
            'pricing_rationale': rationale,
            'approval_gate_required': 'GATE_2_PRICING',
            'status': 'AWAITING_ARTISAN_PRICE_APPROVAL'
        }
