import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from tests.factories import ApplicationFactory, ContactFactory, InterviewFactory

pytestmark = pytest.mark.django_db


class TestApplicationList:
    def test_list_requires_auth(self, api_client):
        response = api_client.get(reverse("application-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_returns_own_applications(self, auth_client, user):
        ApplicationFactory.create_batch(3, owner=user)
        response = auth_client.get(reverse("application-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_excludes_other_users_applications(
        self, auth_client, user, other_user
    ):
        ApplicationFactory(owner=user)
        ApplicationFactory(owner=other_user)
        response = auth_client.get(reverse("application-list"))
        assert len(response.data) == 1

    def test_filter_by_status(self, auth_client, user):
        ApplicationFactory(owner=user, status="applied")
        ApplicationFactory(owner=user, status="interview")
        response = auth_client.get(reverse("application-list"), {"status": "applied"})
        assert len(response.data) == 1
        assert response.data[0]["status"] == "applied"

    def test_filter_by_priority(self, auth_client, user):
        ApplicationFactory(owner=user, priority="high")
        ApplicationFactory(owner=user, priority="low")
        response = auth_client.get(reverse("application-list"), {"priority": "high"})
        assert len(response.data) == 1
        assert response.data[0]["priority"] == "high"

    def test_search_by_company(self, auth_client, user):
        ApplicationFactory(owner=user, company_name="Google")
        ApplicationFactory(owner=user, company_name="Meta")
        response = auth_client.get(reverse("application-list"), {"search": "Google"})
        assert len(response.data) == 1
        assert response.data[0]["company_name"] == "Google"

    def test_search_by_role(self, auth_client, user):
        ApplicationFactory(owner=user, role_title="Backend Engineer")
        ApplicationFactory(owner=user, role_title="Designer")
        response = auth_client.get(reverse("application-list"), {"search": "Backend"})
        assert len(response.data) == 1

    def test_filter_applied_after(self, auth_client, user):
        from datetime import date, timedelta

        ApplicationFactory(owner=user, applied_date=date.today() - timedelta(days=10))
        ApplicationFactory(owner=user, applied_date=date.today() - timedelta(days=2))
        response = auth_client.get(
            reverse("application-list"),
            {"applied_after": (date.today() - timedelta(days=5)).isoformat()},
        )
        assert len(response.data) == 1


class TestApplicationCreate:
    def test_create_application(self, auth_client):
        data = {
            "company_name": "Acme",
            "role_title": "Engineer",
            "status": "applied",
            "priority": "high",
        }
        response = auth_client.post(reverse("application-list"), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["company_name"] == "Acme"

    def test_create_sets_owner_to_current_user(self, auth_client, user):
        data = {"company_name": "X", "role_title": "Y", "status": "wishlist"}
        auth_client.post(reverse("application-list"), data)
        from apps.applications.models import Application

        assert Application.objects.filter(owner=user, company_name="X").exists()

    def test_create_requires_auth(self, api_client):
        response = api_client.post(
            reverse("application-list"), {"company_name": "X", "role_title": "Y"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestApplicationDetail:
    def test_retrieve_own_application(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        response = auth_client.get(reverse("application-detail", args=[app.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert "contacts" in response.data
        assert "interviews" in response.data
        assert "history" in response.data

    def test_cannot_retrieve_other_users_application(self, auth_client, other_user):
        app = ApplicationFactory(owner=other_user)
        response = auth_client.get(reverse("application-detail", args=[app.pk]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_status_creates_history(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="applied")
        response = auth_client.patch(
            reverse("application-detail", args=[app.pk]),
            {"status": "interview"},
        )
        assert response.status_code == status.HTTP_200_OK
        app.refresh_from_db()
        assert app.status == "interview"
        assert app.history.count() == 1
        history = app.history.first()
        assert history.from_status == "applied"
        assert history.to_status == "interview"

    def test_patch_same_status_no_history(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="applied")
        auth_client.patch(
            reverse("application-detail", args=[app.pk]), {"status": "applied"}
        )
        assert app.history.count() == 0

    def test_delete_application(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        response = auth_client.delete(reverse("application-detail", args=[app.pk]))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_cannot_delete_other_users_application(self, auth_client, other_user):
        app = ApplicationFactory(owner=other_user)
        response = auth_client.delete(reverse("application-detail", args=[app.pk]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAdvanceStage:
    def test_advance_wishlist_to_applied(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="wishlist")
        response = auth_client.post(reverse("application-advance", args=[app.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "applied"

    def test_advance_applied_to_phone_screen(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="applied")
        response = auth_client.post(reverse("application-advance", args=[app.pk]))
        assert response.data["status"] == "phone_screen"

    def test_advance_creates_status_history(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="applied")
        auth_client.post(reverse("application-advance", args=[app.pk]))
        app.refresh_from_db()
        assert app.history.count() == 1

    def test_cannot_advance_from_offer(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="offer")
        response = auth_client.post(reverse("application-advance", args=[app.pk]))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_advance_from_rejected(self, auth_client, user):
        app = ApplicationFactory(owner=user, status="rejected")
        response = auth_client.post(reverse("application-advance", args=[app.pk]))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_advance_other_users_application(self, auth_client, other_user):
        app = ApplicationFactory(owner=other_user, status="applied")
        response = auth_client.post(reverse("application-advance", args=[app.pk]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestContacts:
    def test_list_contacts(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        ContactFactory.create_batch(2, application=app)
        response = auth_client.get(reverse("contact-list", args=[app.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_add_contact(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        data = {"name": "Alice", "role": "Recruiter", "email": "alice@example.com"}
        response = auth_client.post(reverse("contact-list", args=[app.pk]), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert app.contacts.count() == 1

    def test_cannot_access_other_users_contacts(self, auth_client, other_user):
        app = ApplicationFactory(owner=other_user)
        response = auth_client.get(reverse("contact-list", args=[app.pk]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_contact(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        contact = ContactFactory(application=app, name="Old Name")
        response = auth_client.patch(
            reverse("contact-detail", args=[app.pk, contact.pk]),
            {"name": "New Name"},
        )
        assert response.status_code == status.HTTP_200_OK
        contact.refresh_from_db()
        assert contact.name == "New Name"

    def test_delete_contact(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        contact = ContactFactory(application=app)
        response = auth_client.delete(
            reverse("contact-detail", args=[app.pk, contact.pk])
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestInterviews:
    def test_add_interview(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        data = {
            "round_number": 1,
            "interview_date": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            "format": "video",
            "notes": "First round",
        }
        response = auth_client.post(reverse("interview-list", args=[app.pk]), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert app.interviews.count() == 1

    def test_cannot_access_other_users_interviews(self, auth_client, other_user):
        app = ApplicationFactory(owner=other_user)
        response = auth_client.get(reverse("interview-list", args=[app.pk]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_interview(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        interview = InterviewFactory(application=app, notes="Old notes")
        response = auth_client.patch(
            reverse("interview-detail", args=[app.pk, interview.pk]),
            {"notes": "Updated notes"},
        )
        assert response.status_code == status.HTTP_200_OK
        interview.refresh_from_db()
        assert interview.notes == "Updated notes"

    def test_delete_interview(self, auth_client, user):
        app = ApplicationFactory(owner=user)
        interview = InterviewFactory(application=app)
        response = auth_client.delete(
            reverse("interview-detail", args=[app.pk, interview.pk])
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
