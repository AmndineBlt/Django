def run(clean=True):
    """Script principal pour générer toutes les données de test"""
    from library.scripts import generate_users, generate_books, generate_reviews, generate_lists_with_entries

    print("🚀 Début de la génération des données de test...")

    if clean:
        print("🧹 Mode nettoyage activé - les anciennes données seront supprimées")

    print("\n👥 Création des utilisateurs...")
    generate_users.run(5, clean=clean)

    print("\n📚 Création des livres...")
    generate_books.run(10, clean=clean)

    print("\n📝 Création des avis...")
    generate_reviews.run(25, clean=clean)

    print("\n📄 Création des listes et entrées...")
    generate_lists_with_entries.run(clean=clean)

    print("\n✅ Données de test générées avec succès.")