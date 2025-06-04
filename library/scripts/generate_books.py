from django.core.management import call_command
from faker import Faker
from library.models import Book
import random

faker = Faker("fr_FR")

def run(n=10):
    """_summary_

    Args:
        n (int, optional): _description_. Defaults to 10.
    """
    for _ in range(n):
        Book.objects.create(
            isbn=faker.isbn13(separator=""),
            title=faker.sentence(nb_words=4),
            author=faker.name(),
            description=faker.paragraph(nb_sentences=3),
            published=str(faker.year()),
            page_count=random.randint(50, 1000),
            rating=round(random.uniform(1, 5), 1)
        )

    print(f"{n} fake books added.")

    # 💾 Dump des données
    with open("library/fixtures/books.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "library.Review", indent=2, stdout=f)
    print("💾 Fixture books.json générée.")