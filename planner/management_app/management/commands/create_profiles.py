import secrets
import string
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from authentication.models import Profile, TechChoices, rolechoices


# (first_name, last_name, username, role, tech)
PROFILES = [
    # Project Coordinators
    ('Anand', 'Varghese', 'anand.varghese', rolechoices.COORDINATOR, None),
    ('Reshma', 'Kurup', 'reshma.kurup', rolechoices.COORDINATOR, None),
    ('Joseph', 'Mathew', 'joseph.mathew', rolechoices.COORDINATOR, None),
    # Backend Developers
    ('Hariprasad', 'Nair', 'hariprasad.nair', rolechoices.DEVELOPER, TechChoices.BACKEND),
    ('Sandeep', 'Menon', 'sandeep.menon', rolechoices.DEVELOPER, TechChoices.BACKEND),
    ('Neethu', 'Balakrishnan', 'neethu.balakrishnan', rolechoices.DEVELOPER, TechChoices.BACKEND),
    # Frontend Developers
    ('Rohit', 'Sharma', 'rohit.sharma', rolechoices.DEVELOPER, TechChoices.FRONTEND),
    ('Anjana', 'Krishna', 'anjana.krishna', rolechoices.DEVELOPER, TechChoices.FRONTEND),
    ('Vishnu', 'Prasad', 'vishnu.prasad', rolechoices.DEVELOPER, TechChoices.FRONTEND),
    # Fullstack Developers
    ('Sreejith', 'Namboothiri', 'sreejith.namboothiri', rolechoices.DEVELOPER, TechChoices.FULLSTACK),
    ('Priya', 'Raghavan', 'priya.raghavan', rolechoices.DEVELOPER, TechChoices.FULLSTACK),
    ('Akhil', 'Chandran', 'akhil.chandran', rolechoices.DEVELOPER, TechChoices.FULLSTACK),
    # UI/UX Designers
    ('Nandana', 'Pillai', 'nandana.pillai', rolechoices.DEVELOPER, TechChoices.UI_UX),
    ('Siddharth', 'Iyer', 'siddharth.iyer', rolechoices.DEVELOPER, TechChoices.UI_UX),
    ('Devika', 'Ramesh', 'devika.ramesh', rolechoices.DEVELOPER, TechChoices.UI_UX),
    # Software Testers
    ('Prakash', 'Kurian', 'prakash.kurian', rolechoices.DEVELOPER, TechChoices.TESTER),
    ('Sreelakshmi', 'Varma', 'sreelakshmi.varma', rolechoices.DEVELOPER, TechChoices.TESTER),
    ('Manu', 'George', 'manu.george', rolechoices.DEVELOPER, TechChoices.TESTER),
]

EMAIL_DOMAIN = 'planner.com'
CREDENTIALS_FILE = Path(settings.BASE_DIR) / 'authentication' / 'credentials.txt'


def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
        ):
            return password


class Command(BaseCommand):
    help = (
        'Create 18 sample Profile records (3 coordinators, 3 backend, 3 frontend, '
        '3 fullstack, 3 UI/UX, 3 testers) and write credentials.txt.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete the sample profiles first if they already exist.',
        )

    def handle(self, *args, **options):
        created = []
        updated = []
        skipped = []

        with transaction.atomic():
            for first_name, last_name, username, role, tech in PROFILES:
                if options['reset']:
                    Profile.objects.filter(username=username).delete()

                existing = Profile.objects.filter(username=username).first()

                if existing:
                    # Keep the current password, only refresh the profile data.
                    existing.first_name = first_name
                    existing.last_name = last_name
                    existing.email = f'{username}@{EMAIL_DOMAIN}'
                    existing.role = role
                    existing.tech = tech
                    existing.save()
                    updated.append(existing)
                    skipped.append(username)
                    continue

                password = generate_password()
                profile = Profile(
                    username=username,
                    email=f'{username}@{EMAIL_DOMAIN}',
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    tech=tech,
                )
                profile.set_password(password)
                profile.save()
                created.append((profile, password))

        self._write_credentials(created)

        self.stdout.write(
            self.style.SUCCESS(
                f'{len(created)} profile(s) created, {len(updated)} updated, '
                f'{len(skipped)} already existed.'
            )
        )
        if skipped:
            self.stdout.write(f'Existing usernames: {", ".join(skipped)}')
        self.stdout.write(f'Credentials written to {CREDENTIALS_FILE}')

    def _write_credentials(self, created):
        lines = [
            'PROJECT PLANNER - SAMPLE PROFILE CREDENTIALS',
            '=' * 60,
            '',
        ]

        if not created:
            lines.append('No new profiles were created in this run.')
        else:
            lines.append(f'{"Username":<22}{"Password":<16}{"Role":<22}{"Tech"}')
            lines.append('-' * 60)
            for profile, password in created:
                lines.append(
                    f'{profile.username:<22}{password:<16}{profile.role:<22}{profile.tech or "-"}'
                )

        lines += [
            '',
            '=' * 60,
            'Note: passwords are shown only once. Change them after first login.',
            '',
        ]

        CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
        CREDENTIALS_FILE.write_text('\n'.join(lines), encoding='utf-8')
