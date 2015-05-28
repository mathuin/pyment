from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# profile.py
# testing order_info below covers this

# views.py
# test my_account (just get)
# test order_details
# test order_info (get and post)


class RegisterTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up For Your Account')

    def test_register_good(self):
        # JMT: for now, only test the good case
        fields = {
            'username': 'testuser',
            'password1': 'testpass!',
            'password2': 'testpass!',
            'email': 'test@example.com',
        }
        response = self.client.post(self.url, fields, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, Testuser!')
