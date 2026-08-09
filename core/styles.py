"""
Komara Agency 🇬🇳 — Gestionnaire de styles visuels
"""

from typing import List, Dict


class StyleManager:
    """Gestionnaire de styles pour Komara Agency 🇬🇳."""

    STYLES: Dict[str, Dict] = {
        "photorealistic": {
            "label": "Photo réaliste",
            "description": "Rendu photographique ultra réaliste, 8K, textures visibles",
            "default": True,
        },
        "portrait_studio": {
            "label": "Portrait studio",
            "description": "Portrait en studio, éclairage pro, fond neutre",
        },
        "lifestyle": {
            "label": "Lifestyle",
            "description": "Scène de vie naturelle, ambiance décontractée",
        },
        "ecommerce": {
            "label": "Produit e-commerce",
            "description": "Photo produit sur fond blanc ou contextuel, haute définition",
        },
        "illustration": {
            "label": "Illustration vectorielle",
            "description": "Illustration style vectoriel, lignes nettes, couleurs plates",
        },
        "3d": {
            "label": "3D",
            "description": "Rendu 3D réaliste, éclairage volumétrique, matériaux PBR",
        },
        "cinematic": {
            "label": "Cinématique",
            "description": "Ambiance cinéma, color grading, lens flare, profondeur",
        },
        "black_white": {
            "label": "Noir et blanc",
            "description": "Photo N&B haut contraste, grain argentique",
        },
        "vintage": {
            "label": "Vintage",
            "description": "Style rétro, tones sépia, grain, vignette",
        },
        "aquarelle": {
            "label": "Aquarelle",
            "description": "Effet peinture aquarelle, textures douces, couleurs diluées",
        },
        "anime": {
            "label": "Anime",
            "description": "Style animation japonaise, lignes nettes, couleurs vives",
        },
        "minimalist": {
            "label": "Minimaliste",
            "description": "Composition épurée, peu d'éléments, espace négatif",
        },
    }

    def list_styles(self) -> List[str]:
        """Retourne la liste des styles disponibles."""
        return list(self.STYLES.keys())

    def list_styles_detailed(self) -> Dict[str, Dict]:
        """Retourne tous les styles avec leurs détails."""
        return self.STYLES

    def is_valid_style(self, style: str) -> bool:
        """Vérifie si un style est valide."""
        return style in self.STYLES

    def get_style_info(self, style: str) -> Dict:
        """Retourne les informations d'un style spécifique."""
        return self.STYLES.get(style, {"error": f"Style '{style}' non trouvé."})

    def get_default_style(self) -> str:
        """Retourne le style par défaut."""
        for key, val in self.STYLES.items():
            if val.get("default", False):
                return key
        return "photorealistic"
