from datetime import datetime
from ..models import db, Approval, Product, Quotation, Negotiation, Order

class GateViolationError(Exception):
    """Raised when an action violates the 3 sovereign artisan approval gates."""
    pass

class ApprovalService:
    @staticmethod
    def record_approval(artisan_id: int, entity_id: int, approval_type: str, decision: str, comments: str = None):
        """
        Records an immutable approval log in the database.
        approval_type: 'GATE_1_CATALOGUE', 'GATE_2_PRICING', 'GATE_3_DEAL'
        decision: 'APPROVE', 'EDIT', 'REJECT'
        """
        approval = Approval(
            entity_id=entity_id,
            artisan_id=artisan_id,
            approval_type=approval_type,
            decision=decision,
            comments=comments,
            timestamp=datetime.utcnow()
        )
        db.session.add(approval)
        db.session.commit()
        return approval

    @staticmethod
    def verify_gate_1_listing(product_id: int) -> bool:
        """Verifies that product listing and story were approved by artisan."""
        product = Product.query.get(product_id)
        if not product or product.status == 'DRAFT':
            return False
        return True

    @staticmethod
    def verify_gate_2_pricing(product_id: int) -> bool:
        """Verifies that listing price and confidential floor were approved."""
        product = Product.query.get(product_id)
        if not product or not product.price_record or not product.price_record.artisan_approved:
            return False
        return product.status == 'ACTIVE_MARKET'

    @staticmethod
    def verify_gate_3_deal(negotiation_id: int) -> bool:
        """Verifies that artisan explicitly signed off on the counteroffer or commercial deal."""
        nego = Negotiation.query.get(negotiation_id)
        if not nego:
            return False
        return nego.artisan_status in ['APPROVED', 'MODIFIED']
