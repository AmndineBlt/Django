from django.core.management import call_command
from django.contrib.auth.models import User
from faker import Faker

faker = Faker('fr_FR')

def run(n=10, clean=False):
    """Génère n utilisateurs de test"""
    if clean:
        print("🧹 Suppression des utilisateurs existants (sauf superusers)...")
        User.objects.filter(is_superuser=False).delete()

    print(f"👥 Génération de {n} nouveaux utilisateurs...")

    created_count = 0
    for _ in range(n):
        username = faker.user_name()
        email = faker.email()
        password = "testpass"

        # Évite les doublons
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, email=email, password=password)
            created_count += 1

    print(f"✅ {created_count} nouveaux utilisateurs créés")
    print(f"📊 Total utilisateurs: {User.objects.count()}")

    # 💾 Dump des données
    with open("library/fixtures/users.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "auth.User", indent=2, stdout=f)
    print("💾 Fixture users.json générée.")