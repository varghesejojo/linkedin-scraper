import os
from django.test import TestCase
from rest_framework.test import APIClient
from dotenv import load_dotenv
load_dotenv() 
class LinkedInAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.invalid_email = os.getenv("LINKEDIN_EMAIL")
        self.invalid_password = os.getenv("LINKEDIN_PASSWORD")

    def test_login_with_invalid_credentials(self):
        response = self.client.post('/login/', {
            'username': self.invalid_email,
            'password': self.invalid_password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)

