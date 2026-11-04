from flask import Blueprint, request, jsonify
from ..models import db, Product, BuyerRequest, Quotation, User

buyer_bp = Blueprint('buyer', __name__, url_prefix='/api/buyer')

@buyer_bp.route('/products', methods=['GET'])
def get_catalogue():
    """
    Public Buyer Catalogue.
    CRITICAL SECURITY ENFORCEMENT: Never exposes confidential_minimum_price or internal costs.
    """
    category = request.args.get('category')
    query = Product.query.filter_by(status='ACTIVE_MARKET')
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    products = query.order_by(Product.product_id.desc()).all()
    # include_confidential=False strictly enforced
    return jsonify([p.to_dict(include_confidential=False) for p in products])

@buyer_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    product = Product.query.get(product_id)
    if not product or product.status != 'ACTIVE_MARKET':
        return jsonify({'error': 'Product not found or not active'}), 404

    # include_confidential=False strictly enforced
    return jsonify(product.to_dict(include_confidential=False))

@buyer_bp.route('/enquiries', methods=['GET', 'POST'])
def manage_enquiries():
    if request.method == 'GET':
        buyer_id = request.args.get('buyer_id', 3)
        reqs = BuyerRequest.query.filter_by(buyer_id=buyer_id).order_by(BuyerRequest.request_id.desc()).all()
        return jsonify([r.to_dict() for r in reqs])

    data = request.json or {}
    buyer_id = data.get('buyer_id', 3)
    product_id = data.get('product_id', 1)
    quantity = data.get('quantity', 1)
    requirements = data.get('requirements', '')
    delivery_location = data.get('delivery_location', 'Pune')

    req = BuyerRequest(
        buyer_id=buyer_id,
        product_id=product_id,
        quantity=quantity,
        requirements=requirements,
        delivery_location=delivery_location,
        status='PENDING'
    )
    db.session.add(req)
    db.session.commit()
    return jsonify(req.to_dict()), 201

@buyer_bp.route('/quotations', methods=['GET'])
def get_buyer_quotations():
    buyer_id = request.args.get('buyer_id', 3)
    quotes = Quotation.query.join(BuyerRequest).filter(BuyerRequest.buyer_id == buyer_id).all()
    return jsonify([q.to_dict() for q in quotes])
