import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from djangoapp.populate import initiate

# Demonstration accounts only. Override passwords with environment variables in production.
DEMO_USERS = [
    ('demo_user', 'Demo', 'User', 'demo.user@example.com'),
    ('emily_carter', 'Emily', 'Carter', 'emily.carter@example.com'),
    ('marcus_lee', 'Marcus', 'Lee', 'marcus.lee@example.com'),
]


class Command(BaseCommand):
    help = 'Creates the root superuser, demo users and the car makes/models data set.'

    def handle(self, *args, **options):
        root_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'Root@Admin2026')
        root, created = User.objects.get_or_create(
            username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'root'),
            defaults={'email': os.getenv('DJANGO_SUPERUSER_EMAIL', 'root@example.com'),
                      'is_staff': True, 'is_superuser': True},
        )
        if created or os.getenv('DJANGO_SUPERUSER_PASSWORD'):
            root.set_password(root_password)
            root.is_staff = root.is_superuser = True
            root.save()
        self.stdout.write(f'Superuser "{root.username}" {"created" if created else "ready"}')

        demo_password = os.getenv('DEMO_USER_PASSWORD', 'Demo@Pass2026')
        for username, first, last, email in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username, defaults={'first_name': first, 'last_name': last, 'email': email}
            )
            if created:
                user.set_password(demo_password)
                user.save()
        self.stdout.write(f'{len(DEMO_USERS)} demo users ready')

        initiate()
        from djangoapp.models import CarMake, CarModel
        self.stdout.write(self.style.SUCCESS(
            f'{CarMake.objects.count()} car makes and {CarModel.objects.count()} car models ready'
        ))
