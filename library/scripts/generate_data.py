def run():
    from library.scripts import generate_users, generate_books, generate_reviews, generate_lists_with_entries

    print("👥 Création des utilisateurs...")
    generate_users.run()

    print("📚 Création des livres...")
    generate_books.run()

    print("📝 Création des avis...")
    generate_reviews.run()

    print("📄 Création des listes et entrées...")
    generate_lists_with_entries.run()

    print("✅ Données de test générées avec succès.")