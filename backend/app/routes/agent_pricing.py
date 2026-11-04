from flask import Blueprint, request, jsonify
from ..models import db, Product, ProductCost, ProductPrice, MarketComparable, Artisan
from ..agents.pricing_agent import MarketPricingAgent
from ..services.approval_service import ApprovalService

agent_pricing_bp = Blueprint('agent_pricing', __name__, url_prefix='/api/agent/pricing')
agent2 = MarketPricingAgent()

@agent_pricing_bp.route('/calculate', methods=['POST'])
def calculate_cost_breakdown():
    data = request.json or {}
    cost_res = agent2.calculate_production_costs(data)
    return jsonify(cost_res)

@agent_pricing_bp.route('/analyze', methods=['POST'])
def analyze_market_and_recommend():
    data = request.json or {}
    category = data.get('category', 'Sarees')
    
    # Calculate costs from artisan input
    cost_data = agent2.calculate_production_costs(data)

    # Fetch curated comparable listings from database
    comps = MarketComparable.query.filter(
        (MarketComparable.category.ilike(f"%{category}%")) | (MarketComparable.category == 'Traditional Saree')
    ).all()
    comp_list = [c.to_dict() for c in comps]

    # Analyze market statistics
    benchmark_data = agent2.analyze_market_benchmarks(comp_list)

    # Generate recommendation & rationale
    recommendation = agent2.generate_pricing_recommendation(cost_data, benchmark_data)

    return jsonify({
        'cost_breakdown': cost_data,
        'market_benchmarks': benchmark_data,
        'recommendation': recommendation
    })

@agent_pricing_bp.route('/comparables/<int:product_id>', methods=['GET'])
def get_product_comparables(product_id):
    product = Product.query.get(product_id)
    category = product.category if product else 'Sarees'

    comps = MarketComparable.query.filter(
        (MarketComparable.category.ilike(f"%{category}%")) | (MarketComparable.category == 'Traditional Saree')
    ).all()
    comp_list = [c.to_dict() for c in comps]
    benchmarks = agent2.analyze_market_benchmarks(comp_list)

    return jsonify({
        'product_id': product_id,
        'category': category,
        'benchmarks': benchmarks
    })

@agent_pricing_bp.route('/approve', methods=['POST'])
def approve_price_gate2():
    """
    APPROVAL GATE 2: Artisan fixes the approved listing price and confidential floor.
    Transitions status: APPROVED_LISTING -> ACTIVE_MARKET.
    """
    data = request.json or {}
    product_id = data.get('product_id', 1)
    approved_price = float(data.get('approved_price', 5000.0))
    confidential_floor = float(data.get('confidential_minimum_price', 4200.0))
    suggested_price = float(data.get('suggested_price', 5000.0))
    suggested_min = float(data.get('suggested_minimum', 4500.0))
    suggested_max = float(data.get('suggested_maximum', 6000.0))
    market_median = float(data.get('market_median', 5200.0))
    rationale = data.get('pricing_rationale', '')

    product = Product.query.get(product_id)
    if not product:
        # Fallback to the latest product
        product = Product.query.order_by(Product.product_id.desc()).first()

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Save costs if provided
    cost_inputs = data.get('cost_inputs', {})
    if cost_inputs:
        cost_calc = agent2.calculate_production_costs(cost_inputs)
        cost_obj = ProductCost.query.filter_by(product_id=product.product_id).first()
        if not cost_obj:
            cost_obj = ProductCost(product_id=product.product_id)
            db.session.add(cost_obj)
        cost_obj.material_cost = cost_calc['material_cost']
        cost_obj.labour_hours = cost_calc['labour_hours']
        cost_obj.labour_rate = cost_calc['labour_rate']
        cost_obj.packaging_cost = cost_calc['packaging_cost']
        cost_obj.other_expenses = cost_calc['other_expenses']
        cost_obj.total_cost = cost_calc['total_cost']
        cost_obj.target_margin = cost_calc['target_margin']

    # Save or update ProductPrice
    price_obj = ProductPrice.query.filter_by(product_id=product.product_id).first()
    if not price_obj:
        price_obj = ProductPrice(product_id=product.product_id)
        db.session.add(price_obj)

    price_obj.suggested_price = suggested_price
    price_obj.suggested_minimum = suggested_min
    price_obj.suggested_maximum = suggested_max
    price_obj.market_median = market_median
    price_obj.approved_price = approved_price
    price_obj.confidential_minimum_price = confidential_floor
    price_obj.pricing_rationale = rationale
    price_obj.artisan_approved = True

    # Update product approved price & publish to ACTIVE_MARKET
    product.approved_price = approved_price
    product.status = 'ACTIVE_MARKET'

    # Log Gate 2 Approval in sovereign audit trail
    ApprovalService.record_approval(
        artisan_id=product.artisan_id,
        entity_id=product.product_id,
        approval_type='GATE_2_PRICING',
        decision='APPROVE',
        comments=f'Artisan fixed public listing price at ₹{approved_price:,.2f} and confidential floor at ₹{confidential_floor:,.2f}.'
    )

    db.session.commit()

    return jsonify({
        'message': 'Gate 2 Cleared: Price approved and product is now live in the marketplace!',
        'product': product.to_dict(include_confidential=True)
    })
