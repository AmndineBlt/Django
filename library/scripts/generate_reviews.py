import random
from django.contrib.auth.models import User
from library.models import Book, Review

def run():
    users = list(User.objects.all())
    books = list(Book.objects.all())

    if not users:
        print("❌ Aucun utilisateur trouvé.")
        return

    if not books:
        print("❌ Aucun livre trouvé.")
        return

    for book in random.sample(books, min(30, len(books))):
        num_reviews = random.randint(1, 3)

        for _ in range(num_reviews):
            user = random.choice(users)
            rating = random.randint(1, 5)
            comment = random.choice([
                "Génial !", "Pas mal", "Bof", "Une lecture difficile", "Un chef-d'œuvre", ""
            ])

            review, created = Review.objects.get_or_create(
                user=user,
                book=book,
                defaults={
                    'rating': rating,
                    'comment': comment
                }
            )

            if created:
                print(f"✅ {user.username} → {book.title} ({rating}⭐)")
            else:
                print(f"⚠️ Review déjà existante : {user.username} → {book.title}")
