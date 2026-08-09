"""
Komara Agency 🇬🇳 — Moteur de génération d'images
"""

import os
import logging
from typing import Dict, Optional


class ImageGenerator:
    """Moteur de génération d'images IA pour Komara Agency 🇬🇳."""

    # Paramètres de qualité par défaut (règles Komara Agency)
    DEFAULT_PARAMS = {
        "resolution": "8K",
        "camera": "Sony A7R V, 85mm lens, f/1.8",
        "lighting": "cinematic soft lighting, golden hour",
        "depth_of_field": "shallow, bokeh background",
        "detail_level": "ultra detailed, skin texture visible, pores, fabric details",
        "palette": "noir, gold, warm tones — luxury African brand aesthetic",
        "style_raw": True,
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("IMAGE_API_KEY", "")

    def generate(
        self,
        prompt: str,
        style: str = "photorealistic",
        aspect_ratio: str = "9:16",
        negative_prompt: Optional[str] = None,
    ) -> Dict:
        """
        Génère une image à partir d'un prompt texte.

        Args:
            prompt: Description de l'image à générer
            style: Style visuel (photorealistic, 3d, cinematic, etc.)
            aspect_ratio: Ratio (9:16, 16:9, 1:1, 4:3)
            negative_prompt: Éléments à éviter

        Returns:
            Dict avec le statut et les infos de l'image générée
        """
        # Construire le prompt complet avec les paramètres de qualité Komara
        full_prompt = self._build_prompt(prompt, style, aspect_ratio)
        neg = negative_prompt or self._default_negative_prompt()

        logging.info("Generating image — style: %s, ratio: %s", style, aspect_ratio)

        # --- Connexion API externe (placeholder) ---
        # Remplacer par l'API de génération de votre choix :
        # - OpenAI DALL-E
        # - Stability AI
        # - Midjourney (via API non officielle)
        # - Replicate
        # - Leonardo.ai

        return {
            "status": "ready",
            "prompt": full_prompt,
            "negative_prompt": neg,
            "style": style,
            "aspect_ratio": aspect_ratio,
            "quality_params": self.DEFAULT_PARAMS,
            "message": "Image prête. Connectez votre API de génération pour activer la production.",
        }

    def _build_prompt(self, prompt: str, style: str, aspect_ratio: str) -> str:
        """Construit le prompt complet avec les paramètres de qualité Komara Agency."""
        base = f"{prompt}, {style}, 8K, ultra detailed, skin texture visible, pores, fabric details"
        camera = f"Shot on Sony A7R V, 85mm lens, f/1.8, shallow depth of field, sharp focus, bokeh background"
        lighting = "cinematic soft lighting, golden hour, luxury African brand aesthetic, noir and gold palette"
        formatting = f"--ar {aspect_ratio} --style raw"

        return f"{base}. {camera}. {lighting}. {formatting}"

    def _default_negative_prompt(self) -> str:
        """Prompt négatif par défaut pour éviter les artefacts."""
        return (
            "deformed faces, extra fingers, six fingers, cartoon, "
            "blurry, low quality, plastic skin, painting effect, "
            "text artifacts, distortion, grain, noise"
        )
