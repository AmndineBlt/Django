from django.core.management import call_command
from faker import Faker
from library.models import Book
import random

faker = Faker("fr_FR")

def run(n=10, clean=False):
    """Génère n livres de test"""
    if clean:
        print("🧹 Suppression des livres existants...")
        Book.objects.all().delete()

    print(f"📚 Génération de {n} nouveaux livres...")

    created_count = 0
    for _ in range(n):
        # Génère un ISBN unique
        isbn = faker.isbn13(separator="")
        attempts = 0
        while Book.objects.filter(isbn=isbn).exists() and attempts < 10:
            isbn = faker.isbn13(separator="")
            attempts += 1

        if attempts < 10:  # Évite les boucles infinies
            Book.objects.create(
                isbn=isbn,
                title=faker.sentence(nb_words=4).replace('.', ''),
                author=faker.name(),
                description=faker.paragraph(nb_sentences=3),
                published=str(faker.year()),
                page_count=random.randint(50, 1000),
                rating=round(random.uniform(1, 5), 1)
            )
            created_count += 1

    print(f"✅ {created_count} nouveaux livres créés")
    print(f"📊 Total livres: {Book.objects.count()}")

    # 💾 Dump des données
    with open("library/fixtures/books.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "library.Book", indent=2, stdout=f)
    print("💾 Fixture books.json générée.")