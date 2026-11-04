from flask import Blueprint, request, jsonify
from ..models import db, Product, ProductImage, ProductStory, Artisan
from ..agents.story_agent import StoryAndCataloguingAgent
from ..services.approval_service import ApprovalService

agent_story_bp = Blueprint('agent_story', __name__, url_prefix='/api/agent/story')
agent1 = StoryAndCataloguingAgent()

@agent_story_bp.route('/transcribe', methods=['POST'])
def transcribe_voice():
    data = request.json or {}
    audio_text = data.get('audio_text', '')
    language = data.get('language', 'mr')

    res = agent1.transcribe_audio(audio_text, language=language)
    return jsonify(res)

@agent_story_bp.route('/generate', methods=['POST'])
def generate_listing_draft():
    """
    Synthesizes voice transcript, image observations, and artisan profile.
    Outputs listing in DRAFT status awaiting Gate 1 approval.
    """
    data = request.json or {}
    audio_text = data.get('audio_text', '')
    language = data.get('language', 'mr')
    image_url = data.get('image_url', 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80')

    artisan = Artisan.query.first()
    artisan_dict = artisan.to_dict() if artisan else {
        'name': 'Meena Tai Jadhav',
        'village': 'Yeola',
        'district': 'Nashik',
        'state': 'Maharashtra',
        'craft_category': 'Paithani Saree Weaving',
        'years_experience': 22
    }

    transcript = agent1.transcribe_audio(audio_text, language=language)
    image_analysis = agent1.analyze_image_attributes(image_url)
    listing_draft = agent1.synthesize_listing(artisan_dict, transcript, image_analysis)

    return jsonify({
        'transcript': transcript,
        'image_analysis': image_analysis,
        'draft': listing_draft
    })

@agent_story_bp.route('/approve', methods=['POST'])
def approve_listing_gate1():
    """
    APPROVAL GATE 1: Artisan reviews and approves the drafted listing.
    Transitions status: DRAFT -> APPROVED_LISTING.
    """
    data = request.json or {}
    title = data.get('title')
    category = data.get('category', 'Sarees')
    description = data.get('description')
    craft_story = data.get('craft_story')
    raw_transcript = data.get('raw_transcript', '')
    english_translation = data.get('english_translation', '')
    language = data.get('language', 'mr')
    image_url = data.get('image_url', 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80')
    production_time = data.get('production_time', 20)

    artisan = Artisan.query.first()
    artisan_id = artisan.artisan_id if artisan else 1

    # Create Product record in APPROVED_LISTING state
    product = Product(
        artisan_id=artisan_id,
        title=title,
        category=category,
        description=description,
        production_time=production_time,
        status='APPROVED_LISTING' # Gate 1 Cleared
    )
    db.session.add(product)
    db.session.flush()

    # Create ProductImage
    img = ProductImage(
        product_id=product.product_id,
        image_url=image_url,
        is_primary=True,
        visual_tags='purple, peacock, zari, handloom, yeola'
    )
    db.session.add(img)

    # Create ProductStory
    story = ProductStory(
        product_id=product.product_id,
        original_transcript=raw_transcript,
        translated_text=english_translation,
        approved_story=craft_story,
        original_language=language,
        artisan_approved=True
    )
    db.session.add(story)

    # Log Gate 1 Approval in sovereign audit trail
    ApprovalService.record_approval(
        artisan_id=artisan_id,
        entity_id=product.product_id,
        approval_type='GATE_1_CATALOGUE',
        decision='APPROVE',
        comments='Artisan reviewed and approved listing title, craft story, and technical specs.'
    )

    db.session.commit()

    return jsonify({
        'message': 'Gate 1 Cleared: Listing successfully approved by artisan!',
        'product': product.to_dict(include_confidential=True)
    }), 201
