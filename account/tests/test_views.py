import re
from allauth.account.admin import EmailAddress, EmailConfirmation
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from test.base_test import TestUsers

from test.factories import EmailFactory, UserFactory


class TestRegistrationView(APITestCase):
    def test_registration(self):
        url = reverse("rest_register")

        data = {
            "username": "gvard",
            "password1": "Bk7^31&3LDXt",
            "password2": "Bk7^31&3LDXt",
            "email": "test@example.com",
        }

        response = self.client.post(
            url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("detail"), "Verification e-mail sent.")
        # FIXME - sometimes fails to send emails?
        self.assertTrue(mail.outbox)

        token_regex = r"registration\/account-confirm-email\/([A-Za-z0-9:\-]+)\/"
        email_content = str(mail.outbox[0].message())

        match = re.search(token_regex, email_content)
        self.assertTrue(match)

        token = match.group(1)

        url = reverse("account_email_verification_sent")
        response = self.client.post(url, {"key": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(EmailAddress.objects.first().verified)

        user = User.objects.first()
        self.assertTrue(Token.objects.filter(user=user).exists())


class TestLoginLogoutViews(APITestCase):
    def test_login_and_logout(self):
        username = "test user"
        password = "pwd123@"
        email = "test@example.com"

        user = UserFactory.create(username=username, password=password, email=email)
        EmailFactory.create(user_id=user.id, email=email)

        url = reverse("rest_login")
        data = {
            "username": username,
            "email": email,
            "password": password,
        }

        response = self.client.post(
            url,
            data=data,
            format="json",
        )
        self.assertTrue(response.data.get("key", None))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("rest_logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserViews(APITestCase):
    fixtures = ["users.json"]

    def test_get_user(self):
        token = TestUsers.get_user1_token()
        data = {
            "pk": 2,
            "username": "user 1",
            "email": "test1@example.com",
            "first_name": "",
            "last_name": "",
        }

        url = reverse("rest_user_details")
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, data)
