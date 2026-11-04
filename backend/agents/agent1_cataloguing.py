# Agent 1: Story & Cataloguing Agent
# Converts regional voice recordings & photos into culturally grounded, professional listings.

from .base_agent import BaseAgent, ApprovalGate
import json

class StoryAndCataloguingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="StoryAndCataloguingAgent", gate=ApprovalGate.GATE_1_CATALOGUE)

    def process_voice_input(self, audio_data: dict, language: str = 'mr') -> dict:
        """
        Simulates Whisper / Indic speech transcription and translation.
        Maintains the original audio, raw transcript, and English translation.
        """
        raw_text = audio_data.get('raw_text', '')
        # Fallback realistic sample for testing Meena's Paithani weave
        if not raw_text and language == 'mr':
            raw_text = "माझं नाव मीना आहे. मी येवल्यामध्ये पारंपारिक पैठणी विणते. ही साडी विणायला २० दिवस लागले. अस्सल रेशीम आणि मोर पल्लू आहे."
        
        # Translation mapping / prompt simulation
        translated_text = audio_data.get('translated_text', '')
        if not translated_text:
            if 'मीना' in raw_text or 'पैठणी' in raw_text:
                translated_text = "My name is Meena. I weave traditional Paithani sarees in Yeola. This saree took 20 days to weave. It has pure silk and peacock pallu."
            else:
                translated_text = f"Transcribed voice recording ({language}): {raw_text}"

        return {
            "original_language": language,
            "raw_transcript": raw_text,
            "english_translation": translated_text
        }

    def analyze_product_images(self, image_urls: list) -> dict:
        """
        Extracts visible characteristics from uploaded photos (motifs, colors, weave patterns).
        Strict Rule: Must distinguish visible observations from artisan-declared claims.
        """
        # In production: invokes CLIP / ViT / Vision LLM
        return {
            "identified_category": "Traditional Handloom Saree",
            "primary_colors": ["Royal Purple", "Golden Zari", "Emerald Green Accents"],
            "visible_motifs": ["Mor (Peacock) Pallu", "Narali (Coconut) Border", "Asawali Creeper Vines"],
            "detected_texture": "Dense silk handloom weave with metallic zari sheen",
            "visual_authenticity_indicators": "Slight organic variance in selvedge characteristic of wooden pit-loom"
        }

    def synthesize_listing_draft(self, artisan_info: dict, voice_result: dict, vision_result: dict) -> dict:
        """
        Synthesizes the artisan voice transcript, artisan background, and image analysis
        into a structured, professional, culturally authentic product listing.
        """
        artisan_name = artisan_info.get('name', 'Artisan')
        village = artisan_info.get('village', 'Yeola')
        state = artisan_info.get('state', 'Maharashtra')
        craft = artisan_info.get('craft_category', 'Handloom Weaving')

        title = f"Handcrafted Royal Purple Paithani Silk Saree with Peacock Zari Pallu"
        
        craft_story = (
            f"Hand-woven with generations of living heritage by master weaver {artisan_name} "
            f"in the historic craft cluster of {village}, {state}. "
            f"Drawing upon {artisan_info.get('years_experience', 15)} years of pit-loom mastery, "
            f"this heirloom piece features traditional {', '.join(vision_result['visible_motifs'])} "
            f"woven with genuine zari thread into rich mulberry silk. "
            f"According to the artisan, every single saree requires approximately 20 uninterrupted days of meticulous hand-shuttle craftsmanship."
        )

        description = (
            f"• Craft: Authentic {craft}\n"
            f"• Origin: {village}, {state}\n"
            f"• Primary Palette: {', '.join(vision_result['primary_colors'])}\n"
            f"• Motifs: Traditional Peacock (Mor) Pallu with Coconut (Narali) border\n"
            f"• Production Cycle: ~20 Days per piece on wooden pit-loom\n"
            f"• Artisan Authenticity: Direct from {artisan_name}'s family workshop, preserving indigenous Maratha royal textile traditions."
        )

        return {
            "title": title,
            "category": "Traditional Saree",
            "description": description,
            "craft_story": craft_story,
            "visible_tags": ["handloom", "paithani", "purple", "peacock_pallu", "pure_silk", "yeola_craft"],
            "status": "DRAFT", # STRICT: Awaiting Gate 1 Artisan Approval
            "requires_approval_gate": ApprovalGate.GATE_1_CATALOGUE.value,
            "message": "AI has generated the product draft. Please review, edit if necessary, and approve before proceeding to pricing."
        }
