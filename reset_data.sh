#!/bin/bash

echo "🧼 Flush de la base..."
python manage.py flush --noinput

sleep 1  # Pause d'1 seconde pour laisser le flush se terminer

echo "📦 Chargement des fixtures..."

FIXTURES=(
    "library/fixtures/users.json"
    "library/fixtures/books.json"
    "library/fixtures/reviews.json"
    "library/fixtures/lists.json"
)

for fixture in "${FIXTURES[@]}"; do
    if [[ -f "$fixture" ]]; then
        echo "➡️  Chargement : $fixture"
        python manage.py loaddata "$fixture" --verbosity 2
    else
        echo "❌ Fichier manquant : $fixture"
    fi
done

sleep 1

echo "👤 Création du superutilisateur..."
python manage.py shell < library/scripts/create_admin.py

echo "✅ Base de données restaurée avec succès !"

# Rendre le script executable : chmod +x reset_data.sh (dans git bash ou wsl)
# Executer le script : ./reset_data.sh