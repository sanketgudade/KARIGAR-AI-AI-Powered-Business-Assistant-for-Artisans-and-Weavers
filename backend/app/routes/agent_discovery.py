from flask import Blueprint, request, jsonify
from ..models import db, Product, BuyerRequest, Quotation, User
from ..agents.discovery_agent import BuyerDiscoveryAndQuotationAgent

agent_discovery_bp = Blueprint('agent_discovery', __name__, url_prefix='/api/agent/discovery')
agent_quotation_bp = Blueprint('agent_quotation', __name__, url_prefix='/api/agent/quotation')
agent3 = BuyerDiscoveryAndQuotationAgent()

@agent_discovery_bp.route('/search', methods=['POST'])
def search_products():
    """
    Agent 3 Visual Similarity Search.
    Finds matching products from the active marketplace catalogue.
    Hides internal costs & confidential floors!
    """
    data = request.json or {}
    query_meta = {
        'tags': data.get('tags', ['purple', 'paithani', 'peacock', 'saree', 'gold_zari']),
        'category': data.get('category', '')
    }

    # Fetch all active products
    active_prods = Product.query.filter_by(status='ACTIVE_MARKET').all()
    # include_confidential=False strictly enforced for buyer-facing search
    catalogue = [p.to_dict(include_confidential=False) for p in active_prods]

    matches = agent3.search_similar_products(query_meta, catalogue)
    return jsonify({
        'query': query_meta,
        'results': matches
    })

@agent_quotation_bp.route('/create', methods=['POST'])
@agent_discovery_bp.route('/quotation/create', methods=['POST'])
def create_preliminary_quotation():
    """
    Generates preliminary tiered bulk quotation for buyer RFQ.
    """
    data = request.json or {}
    product_id = data.get('product_id', 1)
    quantity = int(data.get('quantity', 50))
    buyer_id = data.get('buyer_id', 3) # default Ananya Sharma
    delivery_location = data.get('delivery_location', 'Pune, Maharashtra')
    requirements = data.get('requirements', 'Wholesale Diwali gifting packaging')

    product = Product.query.get(product_id)
    if not product:
        product = Product.query.filter_by(status='ACTIVE_MARKET').first()

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Ensure valid buyer_id
    buyer = User.query.get(buyer_id)
    if not buyer:
        buyer = User.query.filter_by(role='buyer').first()
        buyer_id = buyer.user_id if buyer else 1

    prod_dict = product.to_dict(include_confidential=False)
    quote_calc = agent3.generate_preliminary_quotation(prod_dict, quantity, delivery_location)

    # Record BuyerRequest
    req = BuyerRequest(
        buyer_id=buyer_id,
        product_id=product.product_id,
        quantity=quantity,
        requirements=requirements,
        delivery_location=delivery_location,
        status='QUOTED'
    )
    db.session.add(req)
    db.session.flush()

    # Record Quotation
    quotation = Quotation(
        request_id=req.request_id,
        unit_price=quote_calc['estimated_unit_price'],
        estimated_amount=quote_calc['estimated_total_amount'],
        lead_days=quote_calc['estimated_lead_days'],
        status='PRELIMINARY'
    )
    db.session.add(quotation)
    db.session.commit()

    quote_calc['request_id'] = req.request_id
    quote_calc['quotation_id'] = quotation.quotation_id

    return jsonify(quote_calc), 201
