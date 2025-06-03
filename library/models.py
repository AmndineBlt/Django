"""Models de l'application library.

Ce module contient les modèles suivants :
- Book : un livre avec titre, auteur, ISBN, etc.
- Review : une note et un commentaire associé à un livre et un utilisateur.
- UserList : une liste personnalisée d’un utilisateur (à lire, favoris...).
- ListEntry : une entrée dans une UserList (association livre + date).
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    """
    Représente un livre avec ses informations principales.

    Attributes:
        isbn (str): Numéro ISBN unique du livre.
        title (str): Titre du livre.
        author (str): Auteur du livre.
        description (str): Description optionnelle du livre.
        published (str): Date de publication ou année, au format texte.
        cover_url (ImageField): Image de couverture (optionnelle).
        page_count (int): Nombre de pages du livre.
        rating (float): Note moyenne (optionnelle).
        created_at (datetime): Date de création automatique.
    """

    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published = models.TextField(blank=True)
    cover_url = models.ImageField(blank=True)
    page_count = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Retourne une représentation lisible du livre.

        Returns:
            str: "Titre du livre by Auteur"
        """
        return f"{self.title} by {self.author}"


class Review(models.Model):
    """
    Représente une critique (note/commentaire) laissée par un utilisateur sur un livre.

    Attributes:
        user (User): Utilisateur qui laisse l’avis.
        book (Book): Livre concerné.
        rating (int): Note entre 1 et 5.
        comment (str): Commentaire optionnel.
        created_at (datetime): Date de création automatique.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de l’avis.

        Returns:
            str: "Review by <username> on <book title>"
        """
        return f"Review by {self.user.username} on {self.book.title}"

    def clean(self) -> None:
        """
        Valide la note pour qu'elle soit bien entre 1 et 5.

        Raises:
            ValidationError: Si la note est hors des bornes autorisées.
        """
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")


class UserList(models.Model):
    """
    Représente une liste personnelle d’un utilisateur (par ex. « Favoris », « À lire »...).

    Attributes:
        LIST_CHOICES (list): Liste des types de listes possibles.
        user (User): Utilisateur propriétaire de la liste.
        name (str): Nom de la liste (choisi parmi les LIST_CHOICES).
    """

    LIST_CHOICES = [
        ('read', 'Lu'),
        ('to_read', 'À lire'),
        ('favorite', 'Favoris'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=20, choices=LIST_CHOICES)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de la liste.

        Returns:
            str: "<username> - <nom lisible de la liste>"
        """
        return f"{self.user.username} - {self.get_name_display()}" # type: ignore


class ListEntry(models.Model):
    """
    Représente une entrée dans une liste utilisateur (association d’un livre à une liste).

    Attributes:
        user_list (UserList): La liste dans laquelle le livre est ajouté.
        book (Book): Le livre ajouté.
        added_at (datetime): Date d’ajout automatique.
    """

    user_list = models.ForeignKey(UserList, on_delete=models.CASCADE, related_name='entries')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_list', 'book')

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de l'entrée.

        Returns:
            str: "<Titre du livre> dans <Nom de la liste>"
        """
        return f"{self.book.title} dans {self.user_list}"
