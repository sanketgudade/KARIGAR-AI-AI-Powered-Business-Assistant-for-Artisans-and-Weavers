from flask import Blueprint, request, jsonify
from ..models import db, Product, Quotation, Negotiation, BuyerRequest, Order, Payment, Artisan
from ..agents.negotiation_agent import AINegotiationAgent
from ..services.approval_service import ApprovalService

agent_negotiation_bp = Blueprint('agent_negotiation', __name__, url_prefix='/api/agent/negotiation')
agent4 = AINegotiationAgent()

@agent_negotiation_bp.route('/counteroffer', methods=['POST'])
def submit_buyer_offer():
    """
    Buyer submits a counteroffer (e.g. ₹3,000 for 50 pieces).
    Agent 4 compares it in Python against confidential floor and generates draft counter.
    Status remains strictly PENDING_ARTISAN awaiting Gate 3.
    """
    data = request.json or {}
    quotation_id = data.get('quotation_id', 1)
    buyer_offer = float(data.get('buyer_offer', 3000.0))

    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        quotation = Quotation.query.first()

    if not quotation:
        return jsonify({'error': 'Quotation not found'}), 404

    buyer_req = quotation.buyer_request
    product = buyer_req.product
    artisan = product.artisan

    product_data = {
        'approved_price': product.approved_price or 5000.0,
        'confidential_minimum_price': product.price_record.confidential_minimum_price if product.price_record else 4200.0,
        'total_cost': product.cost.total_cost if product.cost else 2800.0
    }
    artisan_data = {
        'name': artisan.user.name if artisan and artisan.user else 'Meena Tai',
        'craft_category': artisan.craft_category if artisan else 'Paithani Saree Weaving',
        'village': artisan.village if artisan else 'Yeola'
    }

    eval_result = agent4.evaluate_buyer_offer(
        buyer_offer=buyer_offer,
        quantity=buyer_req.quantity,
        product_data=product_data,
        artisan_data=artisan_data
    )

    # Record or update negotiation round
    nego = Negotiation.query.filter_by(quotation_id=quotation.quotation_id).first()
    if not nego:
        nego = Negotiation(quotation_id=quotation.quotation_id)
        db.session.add(nego)

    nego.buyer_offer = buyer_offer
    nego.suggested_counteroffer = eval_result['suggested_counteroffer']
    nego.ai_rationale = eval_result['ai_rationale']
    nego.response_message = eval_result['ai_response_message']
    nego.approved_counteroffer = eval_result['suggested_counteroffer']
    nego.artisan_status = 'PENDING_ARTISAN' # STRICT: Gate 3 hold
    nego.buyer_status = 'PENDING'

    quotation.status = 'NEGOTIATING'
    buyer_req.status = 'NEGOTIATING'

    db.session.commit()

    eval_result['negotiation_id'] = nego.negotiation_id
    eval_result['quotation_id'] = quotation.quotation_id
    return jsonify(eval_result), 200

@agent_negotiation_bp.route('/approve', methods=['POST'])
def artisan_negotiation_approval_gate3():
    """
    APPROVAL GATE 3: Artisan takes sovereign action:
    - 'APPROVE': Transmits AI counteroffer to buyer.
    - 'MODIFY': Customizes price & message, then transmits.
    - 'REJECT': Rejects buyer offer.
    """
    data = request.json or {}
    negotiation_id = data.get('negotiation_id', 1)
    action = data.get('action', 'APPROVE') # 'APPROVE', 'MODIFY', 'REJECT'
    approved_counter = float(data.get('approved_counteroffer', 4500.0))
    custom_message = data.get('custom_message', '')

    nego = Negotiation.query.get(negotiation_id)
    if not nego:
        nego = Negotiation.query.first()

    if not nego:
        return jsonify({'error': 'Negotiation not found'}), 404

    artisan_id = nego.quotation.buyer_request.product.artisan_id

    if action == 'APPROVE':
        nego.artisan_status = 'APPROVED'
        nego.approved_counteroffer = approved_counter
        nego.buyer_status = 'COUNTERED'
    elif action == 'MODIFY':
        nego.artisan_status = 'MODIFIED'
        nego.approved_counteroffer = approved_counter
        if custom_message:
            nego.response_message = custom_message
        nego.buyer_status = 'COUNTERED'
    else:
        nego.artisan_status = 'REJECTED'
        nego.buyer_status = 'REJECTED'

    # Log Gate 3 in sovereign audit trail
    ApprovalService.record_approval(
        artisan_id=artisan_id,
        entity_id=nego.negotiation_id,
        approval_type='GATE_3_DEAL',
        decision=action,
        comments=f'Artisan decided action {action} with counter price ₹{approved_counter:,.2f}.'
    )

    db.session.commit()

    return jsonify({
        'message': f'Gate 3 Cleared: Counteroffer of ₹{approved_counter:,.2f} transmitted to buyer!',
        'negotiation': nego.to_dict(include_rationale=True)
    })

@agent_negotiation_bp.route('/accept-deal', methods=['POST'])
def buyer_accept_counteroffer():
    """
    Buyer accepts the artisan-approved counteroffer.
    Finalizes terms and creates confirmed Order in escrow paid state.
    """
    data = request.json or {}
    negotiation_id = data.get('negotiation_id', 1)

    nego = Negotiation.query.get(negotiation_id)
    if not nego:
        nego = Negotiation.query.first()

    if not nego or nego.artisan_status not in ['APPROVED', 'MODIFIED']:
        return jsonify({'error': 'Deal cannot be finalized without artisan approval.'}), 403

    quotation = nego.quotation
    req = quotation.buyer_request
    product = req.product
    artisan = product.artisan

    agreed_unit_price = nego.approved_counteroffer or 4500.0
    total_amount = agreed_unit_price * req.quantity

    nego.buyer_status = 'ACCEPTED'
    quotation.status = 'ACCEPTED_BY_BUYER'
    quotation.final_amount = total_amount
    req.status = 'ORDERED'

    # Create Confirmed Order
    order = Order(
        quotation_id=quotation.quotation_id,
        buyer_id=req.buyer_id,
        artisan_id=artisan.artisan_id,
        product_id=product.product_id,
        quantity=req.quantity,
        unit_price=agreed_unit_price,
        total_amount=total_amount,
        order_status='PRODUCTION_QUEUED',
        payment_status='ESCROW_PAID' # Simulated payment for hackathon MVP
    )
    db.session.add(order)
    db.session.flush()

    # Create Payment Record
    payment = Payment(
        order_id=order.order_id,
        amount=total_amount,
        payment_status='ESCROW_PAID'
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'message': 'Order successfully confirmed! Escrow advance registered and production queued.',
        'order': order.to_dict()
    }), 201

@agent_negotiation_bp.route('/list', methods=['GET'])
def list_negotiations():
    negos = Negotiation.query.order_by(Negotiation.negotiation_id.desc()).all()
    # include_rationale=True for artisan inbox
    return jsonify([n.to_dict(include_rationale=True) for n in negos])
