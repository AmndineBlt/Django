from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
password = "adminpass"
email = "admin@example.com"

# Supprime l'utilisateur s'il existe déjà (utile après un flush)
User.objects.filter(username=username).delete()

# Crée un superutilisateur
User.objects.create_superuser(username=username, email=email, password=password)

print("✅ Superutilisateur 'admin' recréé.")

# python manage.py shell < library/scripts/create_admin.py