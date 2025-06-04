#!/bin/bash

echo "🧼 Flush de la base..."
python manage.py flush --noinput

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du flush"
    exit 1
fi

echo "📦 Vérification et chargement des fixtures..."

FIXTURES=(
    "library/fixtures/users.json"
    "library/fixtures/books.json" 
    "library/fixtures/reviews.json"
    "library/fixtures/lists_and_entries.json"
)

# Compteur pour savoir si on a chargé au moins une fixture
loaded_count=0

for fixture in "${FIXTURES[@]}"; do
    if [ -f "$fixture" ]; then
        echo "➡️  Chargement : $fixture"
        python manage.py loaddata "$fixture"
        if [ $? -eq 0 ]; then
            ((loaded_count++))
        else
            echo "⚠️  Erreur lors du chargement de $fixture"
        fi
    else
        echo "❌ Fichier manquant : $fixture"
    fi
done

echo "👤 Création du superutilisateur..."
python manage.py shell -c "from library.scripts.create_admin import run; run()"

if [ $loaded_count -eq 0 ]; then
    echo "⚠️  Aucune fixture chargée. Génération de nouvelles données..."
    python manage.py generate_data
fi

echo "✅ Base de données restaurée avec succès !"
echo "📊 Résumé :"
python manage.py shell -c "
from django.contrib.auth.models import User
from library.models import Book, Review, UserList, ListEntry
print(f'  👥 Utilisateurs: {User.objects.count()}')
print(f'  📚 Livres: {Book.objects.count()}')
print(f'  📝 Avis: {Review.objects.count()}')
print(f'  📄 Listes: {UserList.objects.count()}')
print(f'  📋 Entrées: {ListEntry.objects.count()}')
"

# Rendre le script executable : chmod +x reset_data.sh (dans git bash ou wsl)
# Executer le script : ./reset_data.sh