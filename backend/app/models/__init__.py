from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False) # 'artisan', 'buyer', 'admin'
    preferred_language = db.Column(db.String(30), default='mr') # 'mr', 'hi', 'en', 'ta', 'te'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    artisan_profile = db.relationship('Artisan', backref='user', uselist=False, cascade='all, delete-orphan')
    buyer_requests = db.relationship('BuyerRequest', backref='buyer', lazy=True)
    orders = db.relationship('Order', backref='buyer', foreign_keys='Order.buyer_id', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'preferred_language': self.preferred_language,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Artisan(db.Model):
    __tablename__ = 'artisans'
    
    artisan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    craft_category = db.Column(db.String(100), nullable=False) # e.g. 'Paithani Saree Weaving'
    biography = db.Column(db.Text, nullable=True)
    years_experience = db.Column(db.Integer, default=10)
    avatar_url = db.Column(db.String(255), nullable=True)
    
    # Relationships
    products = db.relationship('Product', backref='artisan', lazy=True, cascade='all, delete-orphan')
    artisan_orders = db.relationship('Order', backref='artisan', foreign_keys='Order.artisan_id', lazy=True)
    approvals = db.relationship('Approval', backref='artisan', lazy=True)

    def to_dict(self):
        return {
            'artisan_id': self.artisan_id,
            'user_id': self.user_id,
            'name': self.user.name if self.user else None,
            'phone': self.user.phone if self.user else None,
            'email': self.user.email if self.user else None,
            'preferred_language': self.user.preferred_language if self.user else 'mr',
            'location': self.location,
            'state': self.state,
            'district': self.district,
            'village': self.village,
            'craft_category': self.craft_category,
            'biography': self.biography,
            'years_experience': self.years_experience,
            'avatar_url': self.avatar_url
        }


class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisans.artisan_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    approved_price = db.Column(db.Float, nullable=True)
    availability = db.Column(db.String(50), default='Made to Order') # 'In Stock', 'Made to Order'
    production_time = db.Column(db.Integer, default=20) # in days
    status = db.Column(db.String(50), default='DRAFT') # 'DRAFT', 'APPROVED_LISTING', 'ACTIVE_MARKET', 'ARCHIVED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    story = db.relationship('ProductStory', backref='product', uselist=False, cascade='all, delete-orphan')
    cost = db.relationship('ProductCost', backref='product', uselist=False, cascade='all, delete-orphan')
    price_record = db.relationship('ProductPrice', backref='product', uselist=False, cascade='all, delete-orphan')
    buyer_requests = db.relationship('BuyerRequest', backref='product', lazy=True)
    orders = db.relationship('Order', backref='product', lazy=True)

    def to_dict(self, include_confidential=False):
        """
        SECURITY REQUIREMENT:
        Never expose confidential minimum price or internal cost breakdown to buyers.
        Only included when include_confidential is True (for authorized artisan).
        """
        primary_img = next((img.image_url for img in self.images if img.is_primary), None)
        if not primary_img and self.images:
            primary_img = self.images[0].image_url
            
        res = {
            'product_id': self.product_id,
            'artisan_id': self.artisan_id,
            'artisan_name': self.artisan.user.name if self.artisan and self.artisan.user else 'Master Artisan',
            'artisan_location': f"{self.artisan.village}, {self.artisan.state}" if self.artisan else '',
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'approved_price': self.approved_price,
            'availability': self.availability,
            'production_time': self.production_time,
            'status': self.status,
            'image_url': primary_img,
            'images': [img.to_dict() for img in self.images],
            'story': self.story.to_dict() if self.story else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_confidential:
            res['cost'] = self.cost.to_dict() if self.cost else None
            res['price_record'] = self.price_record.to_dict() if self.price_record else None
            
        return res


class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    embedding_reference = db.Column(db.Text, nullable=True) # Vector or feature string
    is_primary = db.Column(db.Boolean, default=False)
    visual_tags = db.Column(db.Text, nullable=True) # e.g. 'purple, peacock, zari'

    def to_dict(self):
        return {
            'image_id': self.image_id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'visual_tags': self.visual_tags
        }


class ProductStory(db.Model):
    __tablename__ = 'product_stories'
    
    story_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    original_transcript = db.Column(db.Text, nullable=True)
    translated_text = db.Column(db.Text, nullable=True)
    approved_story = db.Column(db.Text, nullable=False)
    original_language = db.Column(db.String(30), default='mr')
    audio_url = db.Column(db.Text, nullable=True)
    artisan_approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'story_id': self.story_id,
            'original_transcript': self.original_transcript,
            'translated_text': self.translated_text,
            'approved_story': self.approved_story,
            'original_language': self.original_language,
            'audio_url': self.audio_url,
            'artisan_approved': self.artisan_approved
        }


class ProductCost(db.Model):
    __tablename__ = 'product_costs'
    
    cost_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False, unique=True)
    material_cost = db.Column(db.Float, nullable=False, default=0.0)
    labour_hours = db.Column(db.Float, nullable=False, default=0.0)
    labour_rate = db.Column(db.Float, nullable=False, default=25.0)
    packaging_cost = db.Column(db.Float, default=100.0)
    other_expenses = db.Column(db.Float, default=200.0)
    total_cost = db.Column(db.Float, nullable=False, default=0.0)
    target_margin = db.Column(db.Float, default=30.0)

    def to_dict(self):
        return {
            'cost_id': self.cost_id,
            'material_cost': self.material_cost,
            'labour_hours': self.labour_hours,
            'labour_rate': self.labour_rate,
            'packaging_cost': self.packaging_cost,
            'other_expenses': self.other_expenses,
            'total_cost': self.total_cost,
            'target_margin': self.target_margin,
            'labour_cost': round(self.labour_hours * self.labour_rate, 2),
            'cost_floor': round(self.total_cost / (1 - (self.target_margin / 100)), 2) if self.target_margin < 100 else self.total_cost
        }


class MarketComparable(db.Model):
    __tablename__ = 'market_comparables'
    
    comparable_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    listed_price = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100), nullable=False) # e.g. 'CraftBazaar Verified Listing'
    retrieval_date = db.Column(db.String(30), default='2026-11-01')
    attributes = db.Column(db.Text, nullable=True) # e.g. 'Peacock Zari Pallu'
    image_url = db.Column(db.Text, nullable=True)
    similarity_score = db.Column(db.Float, default=0.88)

    def to_dict(self):
        return {
            'comparable_id': self.comparable_id,
            'category': self.category,
            'product_name': self.product_name,
            'listed_price': self.listed_price,
            'source': self.source,
            'retrieval_date': self.retrieval_date,
            'attributes': self.attributes,
            'image_url': self.image_url,
            'similarity_score': self.similarity_score
        }


class ProductPrice(db.Model):
    __tablename__ = 'product_prices'
    
    price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False, unique=True)
    suggested_minimum = db.Column(db.Float, nullable=False)
    suggested_maximum = db.Column(db.Float, nullable=False)
    suggested_price = db.Column(db.Float, nullable=False)
    market_median = db.Column(db.Float, nullable=True)
    approved_price = db.Column(db.Float, nullable=True)
    confidential_minimum_price = db.Column(db.Float, nullable=False) # STRICT CONFIDENTIAL
    pricing_rationale = db.Column(db.Text, nullable=True)
    artisan_approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'price_id': self.price_id,
            'suggested_minimum': self.suggested_minimum,
            'suggested_maximum': self.suggested_maximum,
            'suggested_price': self.suggested_price,
            'market_median': self.market_median,
            'approved_price': self.approved_price,
            'confidential_minimum_price': self.confidential_minimum_price,
            'pricing_rationale': self.pricing_rationale,
            'artisan_approved': self.artisan_approved
        }


class BuyerRequest(db.Model):
    __tablename__ = 'buyer_requests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    requirements = db.Column(db.Text, nullable=True)
    delivery_location = db.Column(db.String(150), nullable=True)
    expected_date = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default='PENDING') # 'PENDING', 'QUOTED', 'NEGOTIATING', 'ORDERED', 'CANCELLED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    quotations = db.relationship('Quotation', backref='buyer_request', lazy=True)

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.name if self.buyer else None,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else None,
            'quantity': self.quantity,
            'requirements': self.requirements,
            'delivery_location': self.delivery_location,
            'expected_date': self.expected_date,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Quotation(db.Model):
    __tablename__ = 'quotations'
    
    quotation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('buyer_requests.request_id'), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    estimated_amount = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=True)
    lead_days = db.Column(db.Integer, default=20)
    status = db.Column(db.String(50), default='PRELIMINARY') # 'PRELIMINARY', 'CONFIRMED_BY_ARTISAN', 'ACCEPTED_BY_BUYER', 'REJECTED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    negotiations = db.relationship('Negotiation', backref='quotation', lazy=True)
    orders = db.relationship('Order', backref='quotation', lazy=True)

    def to_dict(self):
        return {
            'quotation_id': self.quotation_id,
            'request_id': self.request_id,
            'unit_price': self.unit_price,
            'estimated_amount': self.estimated_amount,
            'final_amount': self.final_amount,
            'lead_days': self.lead_days,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Negotiation(db.Model):
    __tablename__ = 'negotiations'
    
    negotiation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.quotation_id'), nullable=False)
    round_number = db.Column(db.Integer, default=1)
    buyer_offer = db.Column(db.Float, nullable=False)
    suggested_counteroffer = db.Column(db.Float, nullable=True)
    approved_counteroffer = db.Column(db.Float, nullable=True)
    ai_rationale = db.Column(db.Text, nullable=True)
    response_message = db.Column(db.Text, nullable=True)
    artisan_status = db.Column(db.String(50), default='PENDING_ARTISAN') # 'PENDING_ARTISAN', 'APPROVED', 'MODIFIED', 'REJECTED'
    buyer_status = db.Column(db.String(50), default='PENDING') # 'PENDING', 'ACCEPTED', 'REJECTED', 'COUNTERED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_rationale=False):
        res = {
            'negotiation_id': self.negotiation_id,
            'quotation_id': self.quotation_id,
            'round_number': self.round_number,
            'buyer_offer': self.buyer_offer,
            'approved_counteroffer': self.approved_counteroffer,
            'response_message': self.response_message,
            'artisan_status': self.artisan_status,
            'buyer_status': self.buyer_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_rationale:
            res['suggested_counteroffer'] = self.suggested_counteroffer
            res['ai_rationale'] = self.ai_rationale
        return res


class Approval(db.Model):
    __tablename__ = 'approvals'
    
    approval_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_id = db.Column(db.Integer, nullable=False)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisans.artisan_id'), nullable=False)
    approval_type = db.Column(db.String(50), nullable=False) # 'GATE_1_CATALOGUE', 'GATE_2_PRICING', 'GATE_3_DEAL'
    decision = db.Column(db.String(50), nullable=False) # 'APPROVE', 'EDIT', 'REJECT'
    comments = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'approval_id': self.approval_id,
            'entity_id': self.entity_id,
            'artisan_id': self.artisan_id,
            'approval_type': self.approval_type,
            'decision': self.decision,
            'comments': self.comments,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.quotation_id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisans.artisan_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(50), default='PRODUCTION_QUEUED') # 'PRODUCTION_QUEUED', 'IN_PROGRESS', 'QUALITY_CHECK', 'DISPATCHED', 'DELIVERED'
    payment_status = db.Column(db.String(50), default='PENDING') # 'PENDING', 'ESCROW_PAID', 'RELEASED_TO_ARTISAN'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    payments = db.relationship('Payment', backref='order', lazy=True)

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'quotation_id': self.quotation_id,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.name if self.buyer else None,
            'artisan_id': self.artisan_id,
            'artisan_name': self.artisan.user.name if self.artisan and self.artisan.user else None,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else None,
            'product_image': self.product.images[0].image_url if self.product and self.product.images else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_amount': self.total_amount,
            'order_status': self.order_status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Payment(db.Model):
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='ESCROW_PAID') # 'PENDING', 'ESCROW_PAID', 'RELEASED'
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'amount': self.amount,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        }
