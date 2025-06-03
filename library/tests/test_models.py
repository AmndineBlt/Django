import pytest
from django.contrib.auth.models import User
from library.models import Book, Review
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_review_rating_must_be_between_1_and_5():
    user = User.objects.create_user(username="testuser", password="testpass")
    book = Book.objects.create(
        isbn="9780000000001",
        title="Test Book",
        author="Author",
        page_count=123,
    )

    # Crée une review invalide (note = 6)
    review = Review(user=user, book=book, rating=6)

    # On attend une erreur à la validation
    with pytest.raises(ValidationError):
        review.full_clean()  # Cela lance les validations personnalisées
