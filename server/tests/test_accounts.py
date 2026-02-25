import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestRegister:
    def test_register_creates_user(self, api_client):
        url = reverse("auth-register")
        data = {
            "email": "new@example.com",
            "password": "strongpass1",
            "full_name": "Test User",
            "preferred_language": "en",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.data

    def test_register_duplicate_email_fails(self, api_client, user):
        url = reverse("auth-register")
        data = {
            "email": user.email,
            "password": "strongpass1",
            "full_name": "Dup",
            "preferred_language": "en",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_short_password_fails(self, api_client):
        url = reverse("auth-register")
        data = {"email": "x@example.com", "password": "short", "full_name": "X"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestLogin:
    def test_login_returns_tokens(self, api_client, user):
        response = api_client.post(
            reverse("auth-token"),
            {
                "email": user.email,
                "password": "testpass123",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_wrong_password_returns_401(self, api_client, user):
        response = api_client.post(
            reverse("auth-token"),
            {
                "email": user.email,
                "password": "wrong",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unknown_email_returns_401(self, api_client):
        response = api_client.post(
            reverse("auth-token"),
            {
                "email": "nobody@example.com",
                "password": "testpass123",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestMe:
    def test_me_requires_auth(self, api_client):
        response = api_client.get(reverse("auth-me"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_returns_user_data(self, auth_client, user):
        response = auth_client.get(reverse("auth-me"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert "password" not in response.data

    def test_me_patch_updates_full_name(self, auth_client):
        response = auth_client.patch(reverse("auth-me"), {"full_name": "Updated Name"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["full_name"] == "Updated Name"

    def test_me_patch_updates_language(self, auth_client):
        response = auth_client.patch(reverse("auth-me"), {"preferred_language": "ja"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["preferred_language"] == "ja"

    def test_me_put_not_allowed(self, auth_client):
        response = auth_client.put(reverse("auth-me"), {"full_name": "X"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
