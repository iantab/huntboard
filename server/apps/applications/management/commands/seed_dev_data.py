from datetime import date, timedelta

from apps.accounts.models import User
from apps.applications.models import Application, Contact, Interview
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed the database with demo data for development"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email="demo@huntboard.dev",
            defaults={"full_name": "Demo User", "preferred_language": "en"},
        )
        if created:
            user.set_password("demo1234")
            user.save()
            self.stdout.write(
                self.style.SUCCESS("Created demo user: demo@huntboard.dev / demo1234")
            )
        else:
            self.stdout.write("Demo user already exists — refreshing applications...")

        Application.objects.filter(owner=user).delete()

        today = date.today()

        applications = Application.objects.bulk_create(
            [
                Application(
                    owner=user,
                    company_name="Google",
                    role_title="Senior Backend Engineer",
                    status="interview",
                    priority="high",
                    applied_date=today - timedelta(days=14),
                    notes="Referred by Jane. Strong interest.",
                ),
                Application(
                    owner=user,
                    company_name="Stripe",
                    role_title="Python Engineer",
                    status="phone_screen",
                    priority="high",
                    applied_date=today - timedelta(days=10),
                ),
                Application(
                    owner=user,
                    company_name="Notion",
                    role_title="Full Stack Engineer",
                    status="applied",
                    priority="medium",
                    applied_date=today - timedelta(days=7),
                    follow_up_date=today + timedelta(days=3),
                ),
                Application(
                    owner=user,
                    company_name="Linear",
                    role_title="Frontend Engineer",
                    status="applied",
                    priority="medium",
                    applied_date=today - timedelta(days=5),
                ),
                Application(
                    owner=user,
                    company_name="Vercel",
                    role_title="Developer Experience Engineer",
                    status="wishlist",
                    priority="high",
                ),
                Application(
                    owner=user,
                    company_name="Figma",
                    role_title="Software Engineer",
                    status="offer",
                    priority="high",
                    applied_date=today - timedelta(days=30),
                    salary_min=180000,
                    salary_max=220000,
                ),
                Application(
                    owner=user,
                    company_name="Dropbox",
                    role_title="Backend Engineer",
                    status="rejected",
                    priority="low",
                    applied_date=today - timedelta(days=21),
                ),
                Application(
                    owner=user,
                    company_name="Shopify",
                    role_title="Platform Engineer",
                    status="closed",
                    priority="low",
                    applied_date=today - timedelta(days=45),
                ),
            ]
        )

        google = next(a for a in applications if a.company_name == "Google")
        stripe = next(a for a in applications if a.company_name == "Stripe")

        Contact.objects.create(
            application=google,
            name="Jane Smith",
            role="Recruiter",
            email="jane@google.com",
        )
        Interview.objects.create(
            application=google,
            round_number=1,
            interview_date=timezone.now() - timedelta(days=7),
            format="phone",
            notes="Intro call with recruiter, went well.",
        )
        Interview.objects.create(
            application=google,
            round_number=2,
            interview_date=timezone.now() + timedelta(days=2),
            format="video",
            notes="Technical round — system design.",
        )

        Contact.objects.create(
            application=stripe,
            name="Bob Lee",
            role="Hiring Manager",
            email="bob@stripe.com",
        )
        Interview.objects.create(
            application=stripe,
            round_number=1,
            interview_date=timezone.now() + timedelta(days=1),
            format="video",
            notes="Phone screen scheduled.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(applications)} applications for {user.email}"
            )
        )
