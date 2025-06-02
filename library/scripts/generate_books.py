import random
from library.models import Book

def run():
    for i in range(100):
        isbn = f"978000000{i:04}"

        # get_or_create évite les doublons si l'isbn existe déjà
        book, created = Book.objects.get_or_create(
            isbn=isbn,
            defaults={
                "title": f"Livre {i}",
                "author": "Auteur auto",
                "description": "Livre généré pour test",
                "published": str(1950 + i % 70),
                "page_count": random.randint(100, 800),
                "rating": round(random.uniform(1, 5), 1),
            }
        )

        if created:
            print(f"✅ Livre créé : {book.title}")
        else:
            print(f"⚠️ Déjà existant : {book.title}")
