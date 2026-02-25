import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

APPLICATION_STATUSES = [
    ("wishlist", "Wishlist"),
    ("applied", "Applied"),
    ("phone_screen", "Phone Screen"),
    ("interview", "Interview"),
    ("offer", "Offer"),
    ("rejected", "Rejected"),
    ("closed", "Closed"),
]

PRIORITY_CHOICES = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
]

INTERVIEW_FORMATS = [
    ("phone", "Phone"),
    ("video", "Video"),
    ("onsite", "Onsite"),
    ("take_home", "Take Home"),
]


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    company_name = models.CharField(max_length=255)
    role_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    job_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUSES,
        default="wishlist",
        db_index=True,
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )
    applied_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True, db_index=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.company_name} — {self.role_title}"

    @property
    def is_overdue(self):
        return bool(self.follow_up_date and self.follow_up_date < timezone.now().date())


class StatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="history",
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["changed_at"]

    def __str__(self):
        return f"{self.application} {self.from_status} → {self.to_status}"


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} at {self.application.company_name}"


class Interview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    round_number = models.PositiveIntegerField(default=1)
    interview_date = models.DateTimeField()
    format = models.CharField(max_length=20, choices=INTERVIEW_FORMATS)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["round_number"]

    def __str__(self):
        return f"Round {self.round_number} at {self.application.company_name}"
