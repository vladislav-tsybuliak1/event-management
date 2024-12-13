from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


CREATE_USER_URL = reverse("users:create")
MANAGE_USER_URL = reverse("users:manage")


class PublicUserApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "username": "Test",
            "email": "test@test.com",
            "password": "test123test",
        }

    def test_create_user_success(self) -> None:
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.payload["email"])
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertNotIn("password", response.data)

    def test_create_user_password_too_short(self) -> None:
        self.payload["password"] = "12"
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(email=self.payload["email"])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_user_invalid_username(self) -> None:
        self.payload["username"] = "Test test"
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(email=self.payload["email"])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_user_invalid_email(self) -> None:
        self.payload["email"] = "test.email"
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(email=self.payload["email"])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_user_username_exists(self) -> None:
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_payload = {
            "username": self.payload["username"],
            "email": "new_test@test.com",
            "password": "test123test",
        }
        response = self.client.post(CREATE_USER_URL, new_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(email=new_payload["email"])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_create_user_email_exists(self) -> None:
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_payload = {
            "username": "New_Test",
            "email": self.payload["email"],
            "password": "test123test",
        }
        response = self.client.post(CREATE_USER_URL, new_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model()
            .objects.filter(username=new_payload["username"])
            .exists()
        )
        self.assertFalse(user_exists)


class PrivateUserApiTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            email="test@test.com",
            password="test123test",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.payload = {
            "username": "New_Test",
            "email": "newtest@test.com",
            "password": "newtest123test",
        }

    def test_retrieve_user_info(self) -> None:
        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertNotIn("password", response.data)

    def test_update_user_info(self) -> None:
        response = self.client.put(MANAGE_USER_URL, self.payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, self.payload["username"])
        self.assertEqual(self.user.email, self.payload["email"])
        self.assertTrue(self.user.check_password(self.payload["password"]))

    def test_partial_update_user_info(self) -> None:
        self.payload.pop("password")

        response = self.client.patch(MANAGE_USER_URL, self.payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, self.payload["email"])
        self.assertTrue(self.user.check_password("test123test"))

    def test_unauthorized_user_cannot_access_profile(self) -> None:
        self.client.force_authenticate(user=None)
        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
