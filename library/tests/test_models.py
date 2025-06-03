"""
Tests unitaires pour les modèles de l'application library.

Ce module teste :
- La représentation en chaîne de caractères du modèle Book.
- La validation des notes (rating) pour les avis (Review).
- La création des listes personnalisées de livres (UserList).
- L'ajout de livres dans une liste utilisateur (ListEntry).
- La représentation en chaîne de caractères des entrées de liste.

Chaque test utilise une base de données temporaire grâce au décorateur @pytest.mark.django_db.
"""

import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from library.models import Book, Review, UserList, ListEntry


@pytest.mark.django_db
class TestModels:
    def setup_method(self):
        """
        Initialise les objets de test communs à toutes les méthodes :
        - un utilisateur (User)
        - un livre (Book)
        """
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            isbn="1234567890123",
            title="Test Book",
            author="John Doe",
            description="A test book",
            published="2024",
            page_count=200,
            rating=4.5
        )

    def test_book_str_representation(self):
        """
        Vérifie que la méthode __str__ du modèle Book renvoie
        bien la chaîne attendue.
        """
        assert str(self.book) == "Test Book by John Doe"

    def test_review_rating_valid(self):
        """
        Vérifie qu'une note valide (par exemple 5) ne déclenche
        aucune erreur de validation.
        """
        review = Review(book=self.book, user=self.user, rating=5)
        review.full_clean()  # triggers model validation

    def test_review_rating_invalid(self):
        """
        Vérifie qu'une note invalide (par exemple 10) lève une
        ValidationError comme attendu.
        """
        review = Review(book=self.book, user=self.user, rating=10)
        with pytest.raises(ValidationError):
            review.full_clean()

    def test_user_list_creation(self):
        """
        Vérifie qu'une liste personnalisée (UserList) peut être
        créée et est bien associée à l'utilisateur.
        """
        user_list = UserList.objects.create(user=self.user, name="À lire")
        assert user_list.user == self.user
        assert user_list.name == "À lire"

    def test_list_entry_creation(self):
        """
        Vérifie qu'on peut ajouter un livre dans une liste
        utilisateur via le modèle ListEntry.
        """
        user_list = UserList.objects.create(user=self.user, name="Favoris")
        entry = ListEntry.objects.create(user_list=user_list, book=self.book)
        assert entry.user_list == user_list
        assert entry.book == self.book

    def test_list_entry_str(self):
        """
        Vérifie que la méthode __str__ du modèle ListEntry
        renvoie bien la chaîne attendue (ex : "Test Book dans testuser - Favoris").
        """
        user_list = UserList.objects.create(user=self.user, name="Favoris")
        entry = ListEntry.objects.create(user_list=user_list, book=self.book)
        expected = f"{self.book.title} dans {user_list}"
        assert str(entry) == expected
