from django.core.management import call_command
import random
from django.contrib.auth.models import User
from library.models import Book, UserList, ListEntry

def run(clean=False):
    """Génère des listes et entrées pour tous les utilisateurs"""
    if clean:
        print("🧹 Suppression des listes et entrées existantes...")
        ListEntry.objects.all().delete()
        UserList.objects.all().delete()

    print("📄 Génération des listes et entrées...")

    users = User.objects.filter(is_superuser=False)  # Exclut les superusers
    books = list(Book.objects.all())

    if not books:
        print("❌ Aucun livre trouvé. Générez des livres d'abord.")
        return

    lists_created = 0
    entries_created = 0

    for user in users:
        print(f"👤 Utilisateur : {user.username}")

        # Assurez-vous que UserList.LIST_CHOICES existe dans votre modèle
        for list_type, _ in UserList.LIST_CHOICES:
            user_list, created = UserList.objects.get_or_create(user=user, name=list_type)
            if created:
                print(f"  ✅ Liste créée : {list_type}")
                lists_created += 1
            else:
                print(f"  ⚠️ Liste existante : {list_type}")

            # Sélectionne aléatoirement des livres
            num_books = min(random.randint(3, 6), len(books))
            selected_books = random.sample(books, num_books)

            for book in selected_books:
                entry, created = ListEntry.objects.get_or_create(user_list=user_list, book=book)
                if created:
                    print(f"    📚 Livre ajouté : {book.title}")
                    entries_created += 1
                else:
                    print(f"    ⏩ Déjà présent : {book.title}")

    print(f"✅ {lists_created} nouvelles listes créées")
    print(f"✅ {entries_created} nouvelles entrées créées")
    print(f"📊 Total listes: {UserList.objects.count()}")
    print(f"📊 Total entrées: {ListEntry.objects.count()}")

    with open("library/fixtures/lists_and_entries.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "library.UserList", "library.ListEntry", indent=2, stdout=f)
    print("💾 Fixture lists_and_entries.json générée.")