from django.core.management import call_command
from library.models import Review, Book
from django.contrib.auth.models import User
from faker import Faker
import random

faker = Faker('fr_FR')

def run(n=50, clean=False):
    """Génère n avis de test"""
    if clean:
        print("🧹 Suppression des avis existants...")
        Review.objects.all().delete()

    print(f"📝 Génération de {n} nouveaux avis...")

    users = list(User.objects.filter(is_superuser=False))  # Exclut les superusers
    books = list(Book.objects.all())

    if not users:
        print("❌ Aucun utilisateur trouvé. Générez des utilisateurs d'abord.")
        return

    if not books:
        print("❌ Aucun livre trouvé. Générez des livres d'abord.")
        return

    created_count = 0
    attempts = 0
    max_attempts = n * 3  # Pour éviter les boucles infinies

    while created_count < n and attempts < max_attempts:
        user = random.choice(users)
        book = random.choice(books)
        attempts += 1

        # Évite les doublons (un utilisateur ne peut pas avoir plusieurs avis pour le même livre)
        if not Review.objects.filter(user=user, book=book).exists():
            Review.objects.create(
                user=user,
                book=book,
                rating=random.randint(1, 5),
                comment=faker.sentence()
            )
            created_count += 1

    print(f"✅ {created_count} nouveaux avis créés")
    print(f"📊 Total avis: {Review.objects.count()}")

    # 💾 Dump des données
    with open("library/fixtures/reviews.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "library.Review", indent=2, stdout=f)
    print("💾 Fixture reviews.json générée.")