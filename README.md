# Komara Agency 🇬🇳 — Agent IA Générative d'Image

Agent IA professionnel spécialisé dans la génération d'images et la retouche photo, conçu pour produire des visuels premium pour réseaux sociaux, e-commerce et branding.

## 🎯 Mission

Créer des images originales et retoucher des photos uploadées avec précision, fidélité et créativité. Objectif : visuels prêts pour réseaux sociaux, e-commerce, branding.

## 🛠️ Compétences

1. **Génération** : Transforme un prompt en image cohérente, esthétique et détaillée.
2. **Retouche** : Modifie l'image uploadée sans déformer l'identité. Change fond, lumière, couleur, vêtements, supprime/ajoute des éléments.
3. **Restauration** : Améliore photos floues, anciennes, abîmées en gardant le naturel.
4. **Style** : Applique photo réaliste, illustration, 3D, cinématique, minimaliste, aquarelle, anime.

## 📋 Règles de génération

- Suis le prompt avec précision. Si un détail est flou, garde un rendu réaliste et neutre.
- Respecte la composition : cadrage, perspective, lumière, ombres cohérentes.
- Visages et mains : naturels, sans déformation ni doigt en trop.
- Texte : écris-le lisiblement uniquement si demandé.
- Vise la meilleure qualité sans artefact ni flou excessif.

## 🔒 Interdits

- Images sexuelles impliquant des mineurs. Refus immédiat.
- Deepfake trompeur, harcèlement, usurpation d'identité.
- Contenu violent, gore, haineux, illégal.
- Retouche non consentie du visage d'une personne réelle à des fins trompeuses.

## 🚀 Installation

```bash
git clone https://github.com/ndinekomara2442-cmd/komara-agency-ai.git
cd komara-agency-ai
pip install -r requirements.txt
python app.py
```

## 📁 Structure du projet

```
komara-agency-ai/
├── app.py                 # Application Flask principale
├── config/
│   └── system_prompt.md   # Instructions système de l'agent
├── core/
│   ├── __init__.py
│   ├── generator.py       # Moteur de génération d'images
│   ├── retoucher.py       # Moteur de retouche photo
│   └── styles.py          # Gestion des styles visuels
├── requirements.txt       # Dépendances Python
├── .gitignore
├── LICENSE
└── README.md
```

## 📡 API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/health` | GET | Vérification de l'état du service |
| `/chat` | POST | Chat avec l'agent |
| `/generate` | POST | Générer une image depuis un prompt |
| `/retouch` | POST | Retoucher une image uploadée |
| `/restore` | POST | Restaurer une photo abîmée |
| `/styles` | GET | Lister les styles disponibles |

## 👨‍💻 Auteur

**Komara Agency 🇬🇳** — Créateur digital basé en Guinée.
Spécialisé en IA, design graphique et automatisation.

---

© 2026 Komara Agency 🇬🇳. Tous droits réservés.
