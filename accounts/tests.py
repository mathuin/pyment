from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# profile.py
# testing order_info below covers this

# views.py
# test register -- this gets us .. nothing else
# - both paths (get and post)
# test my_account (just get)
# test order_details
# test order_info (get and post)


class RegisterTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up For Your Account')
