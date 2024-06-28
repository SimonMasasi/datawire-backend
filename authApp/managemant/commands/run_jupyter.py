import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run Jupyter Lab within Django'

    def handle(self, *args, **kwargs):
        subprocess.run(['jupyter', 'lab'])
