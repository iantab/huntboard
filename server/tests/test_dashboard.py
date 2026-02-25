import pytest
from django.urls import reverse
from rest_framework import status
from tests.factories import ApplicationFactory

pytestmark = pytest.mark.django_db


class TestDashboardStats:
    def test_requires_auth(self, api_client):
        response = api_client.get(reverse("dashboard-stats"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_counts_by_stage(self, auth_client, user):
        ApplicationFactory.create_batch(2, owner=user, status="applied")
        ApplicationFactory(owner=user, status="interview")
        response = auth_client.get(reverse("dashboard-stats"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["by_stage"]["applied"] == 2
        assert response.data["by_stage"]["interview"] == 1
        assert response.data["total"] == 3

    def test_all_stages_present_in_response(self, auth_client, user):
        ApplicationFactory(owner=user, status="applied")
        response = auth_client.get(reverse("dashboard-stats"))
        stages = response.data["by_stage"]
        for stage in [
            "wishlist",
            "applied",
            "phone_screen",
            "interview",
            "offer",
            "rejected",
            "closed",
        ]:
            assert stage in stages

    def test_stats_scoped_to_current_user(self, auth_client, user, other_user):
        ApplicationFactory(owner=user, status="applied")
        ApplicationFactory.create_batch(5, owner=other_user, status="applied")
        response = auth_client.get(reverse("dashboard-stats"))
        assert response.data["total"] == 1

    def test_response_rate_zero_when_no_applications(self, auth_client):
        response = auth_client.get(reverse("dashboard-stats"))
        assert response.data["response_rate"] == 0.0

    def test_response_rate_calculation(self, auth_client, user):
        ApplicationFactory.create_batch(4, owner=user, status="applied")
        ApplicationFactory.create_batch(2, owner=user, status="phone_screen")
        response = auth_client.get(reverse("dashboard-stats"))
        # 2 of 6 reached phone_screen or beyond = 33.3%
        assert response.data["response_rate"] == pytest.approx(33.3, rel=0.1)

    def test_avg_days_to_response_is_none_without_history(self, auth_client, user):
        ApplicationFactory(owner=user, status="applied")
        response = auth_client.get(reverse("dashboard-stats"))
        assert response.data["avg_days_to_response"] is None


class TestDashboardActivity:
    def test_requires_auth(self, api_client):
        response = api_client.get(reverse("dashboard-activity"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_list(self, auth_client, user):
        ApplicationFactory.create_batch(3, owner=user)
        response = auth_client.get(reverse("dashboard-activity"))
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_activity_scoped_to_current_user(self, auth_client, user, other_user):
        ApplicationFactory.create_batch(3, owner=other_user)
        response = auth_client.get(reverse("dashboard-activity"))
        total = sum(row["count"] for row in response.data)
        assert total == 0

    def test_activity_includes_recent_applications(self, auth_client, user):
        ApplicationFactory.create_batch(2, owner=user)
        response = auth_client.get(reverse("dashboard-activity"))
        total = sum(row["count"] for row in response.data)
        assert total == 2
