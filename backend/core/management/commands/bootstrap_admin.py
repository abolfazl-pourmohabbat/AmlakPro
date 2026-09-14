import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial Django superuser from environment variables if it does not exist."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()

        # Intentionally do nothing when bootstrap credentials are not configured.
        if not username and not password and not email:
            self.stdout.write("Admin bootstrap skipped: credentials are not configured.")
            return

        if not username or not password:
            raise CommandError(
                "DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must both be set."
            )

        User = get_user_model()
        user = User.objects.filter(username=username).first()

        if user:
            self.stdout.write(f"Admin bootstrap skipped: user '{username}' already exists.")
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Admin bootstrap created superuser '{user.username}'."))
