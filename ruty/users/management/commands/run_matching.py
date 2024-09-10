from django.core.management.base import BaseCommand
from users.matching_algorithm import match_users

class Command(BaseCommand):
    help = 'Run the user matching algorithm'

    def handle(self, *args, **kwargs):
        match_users()
        self.stdout.write(self.style.SUCCESS('Successfully ran matching algorithm'))