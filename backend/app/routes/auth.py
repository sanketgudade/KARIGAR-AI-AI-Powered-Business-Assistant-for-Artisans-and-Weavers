from flask import Blueprint, request, jsonify, session
from ..models import db, User, Artisan

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    password = data.get('password', 'password123')
    role = data.get('role', 'artisan') # 'artisan', 'buyer', 'admin'
    preferred_language = data.get('preferred_language', 'mr')

    if not name or not phone:
        return jsonify({'error': 'Name and phone are required'}), 400

    if User.query.filter((User.phone == phone) | (User.email == email)).first():
        return jsonify({'error': 'User with this phone or email already exists'}), 409

    user = User(
        name=name,
        phone=phone,
        email=email,
        role=role,
        preferred_language=preferred_language
    )
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    if role == 'artisan':
        artisan = Artisan(
            user_id=user.user_id,
            location=data.get('location', 'Yeola, Maharashtra'),
            state=data.get('state', 'Maharashtra'),
            district=data.get('district', 'Nashik'),
            village=data.get('village', 'Yeola'),
            craft_category=data.get('craft_category', 'Paithani Saree Weaving'),
            biography=data.get('biography', 'Master weaver preserving traditional handloom heritage.'),
            years_experience=data.get('years_experience', 15),
            avatar_url=data.get('avatar_url', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80')
        )
        db.session.add(artisan)

    db.session.commit()
    return jsonify({
        'message': 'Registration successful',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    phone = data.get('phone')
    email = data.get('email')
    password = data.get('password')

    user = None
    if phone:
        user = User.query.filter_by(phone=phone).first()
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        # Fallback to Meena Tai for demo convenience if no params given
        user = User.query.filter_by(role='artisan').first()

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    if password and not user.check_password(password):
        # Demo bypass for development convenience if 'password123' or 'rajkumar@123'
        if password not in ['password123', 'rajkumar@123']:
            return jsonify({'error': 'Invalid password'}), 401

    artisan_data = user.artisan_profile.to_dict() if user.artisan_profile else None

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'artisan': artisan_data
    })

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    # Retrieve user from query param or header for demo simplicity
    phone = request.args.get('phone', '9823011223') # default Meena Tai
    user = User.query.filter_by(phone=phone).first()
    if not user:
        user = User.query.first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user': user.to_dict(),
        'artisan': user.artisan_profile.to_dict() if user.artisan_profile else None
    })
