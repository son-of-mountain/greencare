#!/bin/bash

# Script pour ajouter des exemples d'actions RSE hospitalières
# Usage: ./add_sample_actions.sh

API_URL="http://localhost:8000/api"

echo "🌱 Ajout d'actions RSE d'exemple dans GreenCare..."
echo ""

# Action 1 - Énergie
echo "➤ Ajout : Extinction automatique des écrans..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Extinction automatique des écrans en radiologie",
    "description": "Installer des capteurs de présence pour éteindre automatiquement les écrans PACS et les postes de travail en radiologie après 10 minutes d inactivité. Réduction de 30% de la consommation électrique du service.",
    "service_id": "Radiologie",
    "category": "Énergie",
    "image_url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800",
    "gain_kwh": 450,
    "gain_euro": 225,
    "gain_co2": 180
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 2 - Déchets
echo "➤ Ajout : Tri sélectif bloc opératoire..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tri sélectif renforcé au bloc opératoire",
    "description": "Mise en place de poubelles de tri pour séparer les DASRI, les déchets recyclables (cartons, plastiques propres) et les déchets ordinaires. Formation des équipes sur les bonnes pratiques de tri.",
    "service_id": "Bloc Opératoire",
    "category": "Déchets",
    "image_url": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800",
    "gain_kwh": 0,
    "gain_euro": 850,
    "gain_co2": 420
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 3 - Énergie
echo "➤ Ajout : LED dans les couloirs..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Remplacement par LED dans tous les couloirs",
    "description": "Remplacer les tubes néons classiques par des LED à détecteur de mouvement dans les couloirs, escaliers et zones de circulation. Durée de vie 10x supérieure et consommation divisée par 3.",
    "service_id": "Services Généraux",
    "category": "Énergie",
    "image_url": "https://images.unsplash.com/photo-1513828583688-c52646db42da?w=800",
    "gain_kwh": 1200,
    "gain_euro": 600,
    "gain_co2": 480
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 4 - Transport
echo "➤ Ajout : Covoiturage personnel..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Plateforme de covoiturage pour le personnel",
    "description": "Créer une application de covoiturage interne pour faciliter le partage de trajets domicile-travail. Incitation financière de 50€/mois pour les covoitureurs réguliers. Objectif : 100 agents participants.",
    "service_id": "Direction RH",
    "category": "Transport",
    "image_url": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800",
    "gain_kwh": 0,
    "gain_euro": 0,
    "gain_co2": 2500
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 5 - Numérique
echo "➤ Ajout : Optimisation serveurs..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Virtualisation et optimisation des serveurs",
    "description": "Migrer 15 serveurs physiques vers une infrastructure virtualisée mutualisée. Réduction de 60% de la consommation électrique de la salle serveurs et amélioration de la disponibilité.",
    "service_id": "DSI",
    "category": "Numérique",
    "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800",
    "gain_kwh": 3500,
    "gain_euro": 1750,
    "gain_co2": 1400
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 6 - Alimentation
echo "➤ Ajout : Circuit court restauration..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Approvisionnement local bio pour la cuisine centrale",
    "description": "Passer à 50% de produits locaux (rayon 50km) et 30% de produits bio pour les repas patients et personnel. Partenariat avec 5 producteurs locaux. Réduction des émissions de transport et soutien à l économie locale.",
    "service_id": "Restauration",
    "category": "Alimentation",
    "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
    "gain_kwh": 0,
    "gain_euro": 0,
    "gain_co2": 800
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 7 - Eau
echo "➤ Ajout : Récupération eau de pluie..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Récupération eau de pluie pour espaces verts",
    "description": "Installer 3 cuves de 5000L pour récupérer les eaux pluviales des toits et les utiliser pour arroser les espaces verts et jardins thérapeutiques. Économie de 45000L eau potable par an.",
    "service_id": "Services Techniques",
    "category": "Eau",
    "image_url": "https://images.unsplash.com/photo-1541975250-e5bf0ab94cf5?w=800",
    "gain_kwh": 0,
    "gain_euro": 180,
    "gain_co2": 15
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 8 - Déchets
echo "➤ Ajout : Compostage restauration..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Compostage des déchets organiques de la cuisine",
    "description": "Mettre en place un système de compostage pour valoriser les épluchures et restes alimentaires de la cuisine centrale. Production de compost pour les espaces verts. Réduction de 40% du volume de déchets ordinaires.",
    "service_id": "Restauration",
    "category": "Déchets",
    "image_url": "https://images.unsplash.com/photo-1611348524140-53c9a25263d6?w=800",
    "gain_kwh": 0,
    "gain_euro": 320,
    "gain_co2": 280
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 9 - Énergie
echo "➤ Ajout : Panneaux solaires parking..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ombrières photovoltaïques sur parking personnel",
    "description": "Installer 2000m² de panneaux solaires sur le parking de 250 places. Production de 300 MWh/an couvrant 15% des besoins électriques de l hôpital. Double bénéfice : production d énergie + protection véhicules.",
    "service_id": "Direction",
    "category": "Énergie",
    "image_url": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800",
    "gain_kwh": 300000,
    "gain_euro": 45000,
    "gain_co2": 120000
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 10 - Bien-être
echo "➤ Ajout : Salle de repos personnel..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aménagement de salles de repos avec lumière naturelle",
    "description": "Créer 3 espaces de repos confortables avec lumière naturelle, plantes, fauteuils ergonomiques et coin tisanerie pour le personnel soignant. Amélioration du bien-être et réduction du stress.",
    "service_id": "Direction RH",
    "category": "Bien-être",
    "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800",
    "gain_kwh": 0,
    "gain_euro": 0,
    "gain_co2": 0
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 11 - Chauffage
echo "➤ Ajout : Régulation intelligente chauffage..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Système de régulation intelligente du chauffage",
    "description": "Installer des thermostats connectés et une GTB (Gestion Technique du Bâtiment) pour optimiser le chauffage selon l occupation réelle des zones. Réduction de 25% de la consommation de gaz.",
    "service_id": "Services Techniques",
    "category": "Énergie",
    "image_url": "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=800",
    "gain_kwh": 5800,
    "gain_euro": 2900,
    "gain_co2": 2320
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

# Action 12 - Matériel
echo "➤ Ajout : Don matériel médical..."
curl -X POST "$API_URL/actions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Programme de don de matériel médical réformé",
    "description": "Établir des partenariats avec des ONG pour donner le matériel médical encore fonctionnel mais réformé (lits, fauteuils, petit matériel). Éviter la mise en décharge et prolonger la durée de vie.",
    "service_id": "Logistique",
    "category": "Déchets",
    "image_url": "https://images.unsplash.com/photo-1584515933487-779824d29309?w=800",
    "gain_kwh": 0,
    "gain_euro": 0,
    "gain_co2": 650
  }' \
  -w "\n" -s > /dev/null

echo "✓ Action ajoutée"
echo ""

echo "✅ 12 actions d'exemple ajoutées avec succès !"
echo ""
echo "📊 Catégories couvertes :"
echo "   • Énergie (5 actions)"
echo "   • Déchets (4 actions)"
echo "   • Transport (1 action)"
echo "   • Numérique (1 action)"
echo "   • Alimentation (1 action)"
echo "   • Eau (1 action)"
echo "   • Bien-être (1 action)"
echo ""
echo "🌐 Rendez-vous sur http://localhost:8000/app/index.html pour voir les actions !"
