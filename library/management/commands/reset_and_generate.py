from django.core.management.base import BaseCommand
from django.core.management import call_command
from library.scripts import generate_data, create_admin

class Command(BaseCommand):
    help = 'Reset la base de données et génère des données de test'

    def handle(self, *args, **options):
        self.stdout.write("🧼 Flush de la base...")
        call_command('flush', '--noinput')

        self.stdout.write("🚀 Génération des données...")
        generate_data.run()

        self.stdout.write("👤 Création du superutilisateur...")
        create_admin.run()

        self.stdout.write(self.style.SUCCESS('✅ Base de données réinitialisée avec succès !'))