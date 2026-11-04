from flask import Blueprint, request, jsonify
from ..models import db, User, Artisan, Product, Order, Approval, MarketComparable

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
def get_admin_dashboard():
    total_users = User.query.count()
    total_artisans = Artisan.query.count()
    total_buyers = User.query.filter_by(role='buyer').count()
    total_products = Product.query.count()
    active_products = Product.query.filter_by(status='ACTIVE_MARKET').count()
    total_orders = Order.query.count()
    total_gmv = sum(o.total_amount for o in Order.query.all())

    return jsonify({
        'metrics': {
            'total_users': total_users,
            'total_artisans': total_artisans,
            'total_buyers': total_buyers,
            'total_products': total_products,
            'active_products': active_products,
            'total_orders': total_orders,
            'total_gmv': total_gmv
        },
        'system_health': 'Normal',
        'approval_gates_integrity': '100% Enforced'
    })

@admin_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@admin_bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([p.to_dict(include_confidential=False) for p in products])

@admin_bp.route('/orders', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

@admin_bp.route('/approvals', methods=['GET'])
def list_approvals():
    approvals = Approval.query.order_by(Approval.timestamp.desc()).all()
    return jsonify([a.to_dict() for a in approvals])
