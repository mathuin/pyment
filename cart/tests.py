from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# admin.py
# write silly test for management command to delete_old_carts
# write tests for processing and cancelling orders from web
# write silly test identifying an order's picklist
# write test for processing and cancelling picklists from web
# write silly test identifying a picklist's order

# checkout.py
# write test for creating and cancelling order
# - bonus points for doing email right
# write silly test trying to cancel a fulfilled picklist

# cart.py
# write test for adding to cart
# write test for updating quantity in cart (adding and removing)


class ViewTest(TestCase):
    def setUp(self):
        self.url = reverse('show_cart')

    def test_show_cart_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your cart is empty.')
