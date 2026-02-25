import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("company_name", models.CharField(max_length=255)),
                ("role_title", models.CharField(max_length=255)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("job_url", models.URLField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("wishlist", "Wishlist"),
                            ("applied", "Applied"),
                            ("phone_screen", "Phone Screen"),
                            ("interview", "Interview"),
                            ("offer", "Offer"),
                            ("rejected", "Rejected"),
                            ("closed", "Closed"),
                        ],
                        default="wishlist",
                        max_length=20,
                    ),
                ),
                ("applied_date", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("role", models.CharField(blank=True, max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("linkedin_url", models.URLField(blank=True)),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="applications.application",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Interview",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("round_number", models.PositiveIntegerField(default=1)),
                ("interview_date", models.DateTimeField()),
                (
                    "format",
                    models.CharField(
                        choices=[
                            ("phone", "Phone"),
                            ("video", "Video"),
                            ("onsite", "Onsite"),
                            ("take_home", "Take Home"),
                        ],
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interviews",
                        to="applications.application",
                    ),
                ),
            ],
            options={
                "ordering": ["round_number"],
            },
        ),
    ]
