#!/bin/bash

echo "🚀 Génération des données et reset complet..."

echo "📊 Génération des fixtures..."
python manage.py shell -c "from library.scripts.generate_data import run; run()"

if [ $? -eq 0 ]; then
    echo "✅ Fixtures générées avec succès"
    echo "🔄 Reset de la base avec les nouvelles données..."
    ./reset_data.sh
else
    echo "❌ Erreur lors de la génération des fixtures"
    exit 1
fi