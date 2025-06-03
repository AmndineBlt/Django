from django.contrib.auth.models import User

def run():
    for i in range(10):
        username = f"user{i}"
        password = "azerty123"

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            print(f"✅ Utilisateur créé : {username} / mot de passe : {password}")
        else:
            print(f"⚠️ Utilisateur déjà existant : {username}")
