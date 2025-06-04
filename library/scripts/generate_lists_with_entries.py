from django.core.management import call_command
import random
from django.contrib.auth.models import User
from library.models import Book, UserList, ListEntry

def run():
    users = User.objects.all()
    books = list(Book.objects.all())

    if not books:
        print("❌ Aucun livre trouvé. Ajoute des livres avant de générer les listes.")
        return

    for user in users:
        print(f"👤 Utilisateur : {user.username}")
        for list_type, _ in UserList.LIST_CHOICES:
            user_list, created = UserList.objects.get_or_create(user=user, name=list_type)
            if created:
                print(f"  ✅ Liste créée : {list_type}")
            else:
                print(f"  ⚠️ Liste existante : {list_type}")

            selected_books = random.sample(books, random.randint(3, 6))

            for book in selected_books:
                entry, created = ListEntry.objects.get_or_create(user_list=user_list, book=book)
                if created:
                    print(f"    📚 Livre ajouté : {book.title}")
                else:
                    print(f"    ⏩ Déjà présent : {book.title}")

    with open("library/fixtures/lists_and_entries.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "library.UserList", "library.ListEntry", indent=2, stdout=f)
    print("💾 Fixture lists_and_entries.json générée.")