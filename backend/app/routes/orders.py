from flask import Blueprint, request, jsonify
from ..models import db, Order, Payment

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('', methods=['GET'])
def get_orders():
    artisan_id = request.args.get('artisan_id')
    buyer_id = request.args.get('buyer_id')

    query = Order.query
    if artisan_id:
        query = query.filter_by(artisan_id=artisan_id)
    if buyer_id:
        query = query.filter_by(buyer_id=buyer_id)

    orders = query.order_by(Order.order_id.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order_detail(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.to_dict())

@order_bp.route('/update-status', methods=['POST'])
def update_order_status():
    data = request.json or {}
    order_id = data.get('order_id')
    new_status = data.get('order_status') # 'IN_PROGRESS', 'QUALITY_CHECK', 'DISPATCHED', 'DELIVERED'

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.order_status = new_status
    if new_status == 'DELIVERED':
        order.payment_status = 'RELEASED_TO_ARTISAN'

    db.session.commit()
    return jsonify({'message': 'Order stage updated', 'order': order.to_dict()})
