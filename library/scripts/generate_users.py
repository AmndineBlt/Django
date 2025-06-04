from django.core.management import call_command
from django.contrib.auth.models import User
from faker import Faker

faker = Faker('fr_FR')

def run(n=10):
    """_summary_

    Args:
        n (int, optional): _description_. Defaults to 10.
    """
    for _ in range(n):
        username = faker.user_name()
        email = faker.email()
        password = "testpass"
        User.objects.create_user(username=username, email=email, password=password)
    print(f"✅ {n} utilisateurs générés")

    # 💾 Dump des données
    with open("library/fixtures/users.json", "w", encoding="utf-8") as f:
        call_command("dumpdata", "auth.User", indent=2, stdout=f)
    print("💾 Fixture users.json générée.")