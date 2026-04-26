"""
Management command to create or update a platform user with specified role.

Unlike create_superuser (which reads env vars), this accepts explicit CLI
arguments so it can be called from the LCC Manager GUI or CI scripts.

Usage:
    python manage.py seed_platform_user --email admin@lcc.lk --password Secret123
    python manage.py seed_platform_user --email staff@lcc.lk --password Secret123 --role platform_admin
    python manage.py seed_platform_user --email viewer@lcc.lk --password Secret123 --role viewer --update
"""

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Create or update a platform user with the given credentials and role."""

    help = (
        "Create or update a PlatformUser. Idempotent by default — skips if "
        "the email exists. Use --update to force password/role update."
    )

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True, type=str, help="User email address")
        parser.add_argument("--password", required=True, type=str, help="User password (min 8 chars)")
        parser.add_argument("--first-name", dest="first_name", default="Platform", type=str)
        parser.add_argument("--last-name", dest="last_name", default="Admin", type=str)
        parser.add_argument(
            "--role",
            default="super_admin",
            choices=["super_admin", "platform_admin", "support", "viewer"],
            help="Platform role (default: super_admin)",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            default=False,
            help="If user exists, update password and role instead of skipping.",
        )

    def handle(self, *args, **options):
        from apps.platform.models import PlatformUser  # local import avoids circular issues

        email = options["email"].strip().lower()
        password = options["password"]
        first_name = options["first_name"]
        last_name = options["last_name"]
        role = options["role"]
        do_update = options["update"]

        # Basic validation
        if len(password) < 8:
            raise CommandError("Password must be at least 8 characters long.")

        try:
            user = PlatformUser.objects.get(email=email)
        except PlatformUser.DoesNotExist:
            user = None

        if user is not None:
            if not do_update:
                self.stdout.write(
                    self.style.WARNING(
                        f"Platform user '{email}' already exists. "
                        "Use --update to overwrite password/role."
                    )
                )
                return
            # Update existing
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.role = role
            user.is_active = True
            if role == "super_admin":
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_superuser = False
                user.is_staff = role in ("platform_admin", "support")
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Updated platform user: {email}  (role={role})")
            )
        else:
            # Create new
            if role == "super_admin":
                user = PlatformUser.objects.create_superuser(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
            else:
                user = PlatformUser(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    is_active=True,
                    is_staff=role in ("platform_admin", "support"),
                    is_superuser=False,
                )
                user.set_password(password)
                user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Created platform user: {email}  (role={role})")
            )

        # Always show final state
        self.stdout.write(f"  Email     : {user.email}")
        self.stdout.write(f"  Role      : {user.role}")
        self.stdout.write(f"  is_active : {user.is_active}")
        self.stdout.write(f"  is_staff  : {user.is_staff}")
        self.stdout.write(f"  is_superuser : {user.is_superuser}")
