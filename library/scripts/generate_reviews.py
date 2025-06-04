from django.core.management import call_command
from library.models import Review, Book
from django.contrib.auth.models import User
from faker import Faker
import random

faker = Faker('fr_FR')

def run(n=50):
    """_summary_

    Args:
        n (int, optional): _description_. Defaults to 50.
    """
    users = list(User.objects.all())
    books = list(Book.objects.all())

    for _ in range(n):
        Review.objects.create(
            user=random.choice(users),
            book=random.choice(books),
            rating=random.randint(1, 5),
            comment=faker.sentence()
        )
    print(f"✅ {n} avis générés")

    # 💾 Dump des données
    with open("library/fixtures/reviews.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "library.Book", indent=2, stdout=f)
    print("💾 Fixture reviews.json générée.")