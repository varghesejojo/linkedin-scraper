from django.test import TestCase
from rest_framework.test import APIClient

class LinkedInAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_with_invalid_credentials(self):
        response = self.client.post('/login/', {
            'username': 'your_email@example.com',
            'password': 'your_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)

