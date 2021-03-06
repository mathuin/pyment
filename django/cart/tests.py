from django.test import TestCase

# from django.core.management import call_command
# from django.core.management.base import CommandError
# from django.core.exceptions import ValidationError
from django.urls import reverse

# cart.py
# write test for adding to cart
# write test for updating quantity in cart (adding and removing)
# write test for continuing shopping
# write test for empty cart


class ViewTest(TestCase):
    def setUp(self):
        self.url = reverse("cart:show_cart")

    def test_show_cart_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart is empty.")
