from django.core.management.base import BaseCommand
from library.scripts import generate_data

class Command(BaseCommand):
    help = 'Génère des données de test pour la bibliothèque'

    def handle(self, *args, **options):
        generate_data.run()
        self.stdout.write(self.style.SUCCESS('Données générées avec succès'))