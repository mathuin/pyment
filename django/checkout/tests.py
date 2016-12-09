from django.test import TestCase, Client
import http.client
from checkout.models import Order, PickList
from meadery.models import Product
from checkout.checkout import all_in_stock, create_picklist, process_picklist, cancel_picklist

# admin.py
# write tests for processing and cancelling orders from web
# write silly test identifying an order's picklist
# write test for processing and cancelling picklists from web
# write silly test identifying a picklist's order

# checkout.py
# write test for creating and cancelling order
# - bonus points for doing email right
# write silly test trying to cancel a fulfilled picklist

# forms.py
# test clean_phone, which will test strip_non_numbers

# models.py
# printstatus for orders
# orderitems properties
# picklist str and absoluteurl (email!)
# picklistitem properties and absoluteurl (email!)

# checkout_tags.py
# having a real order will be enough I suspect

# views
# showcheckout (get and post, logged in and not)
# receipt?!?


class OrderTestCase(TestCase):
    fixtures = ['accounts', 'meadery', 'inventory', 'checkout']

    def setUp(self):
        self.order = Order.objects.all()[0]
        self.client = Client()

    def test_permalink(self):
        url = self.order.get_absolute_url()
        response = self.client.get(url)
        self.assertTrue(response)
        # not OK, but FOUND (302, redirect)
        self.assertEqual(response.status_code, http.client.FOUND)
        # FIXME: check that it redirects the right place

    def test_str(self):
        self.assertEqual(self.order.__str__(), 'Order #' + str(self.order.id))

    # FIXME: test show_checkout somehow?

    # FIXME: test receipt like category views

    # FIXME: test create_order
    def test_create_order(self):
        # FIXME: learn how to create an order from a request
        return True

    def test_all_in_stock(self):
        # requires order #1 to be valid
        checkval = all_in_stock(self.order)
        self.assertTrue(checkval)
        # requires order #2 to be invalid
        # (requests 1 jar of product 2 which is not in stock)
        order2 = Order.objects.all()[1]
        checkval2 = all_in_stock(order2)
        self.assertFalse(checkval2)

    def test_create_picklist(self):
        # confirm both jars are marked active and available
        sip1a = Product.active.get(slug='sip-1-a')
        self.assertEqual(sip1a.jar_set.filter(is_active=True).count(), 14)
        self.assertEqual(sip1a.jar_set.filter(is_available=True).count(), 14)
        # generate valid picklist from order #1
        picklist = create_picklist(self.order)
        self.assertEqual(sip1a.jar_set.filter(is_available=True).count(), 12)
        self.assertEqual(picklist.status, PickList.SUBMITTED)
        self.assertEqual(self.order.status, Order.PROCESSED)
        # try to generate another picklist from order #1
        # (should fail as status should have changed)
        picklist_again = create_picklist(self.order)
        self.assertEqual(picklist_again, None)
        # try to generate picklist from order #2
        # (should fail as no product exists)
        order2 = Order.objects.all()[1]
        picklist2 = create_picklist(order2)
        self.assertEqual(picklist2, None)

    # FIXME: check process_picklist
    def test_process_picklist(self):
        # confirm both jars are marked available and active
        sip1a = Product.active.get(slug='sip-1-a')
        self.assertEqual(sip1a.jar_set.filter(is_active=True).count(), 14)
        self.assertEqual(sip1a.jar_set.filter(is_available=True).count(), 14)
        # generate valid picklist from order #1
        picklist = create_picklist(self.order)
        retval = process_picklist(picklist)
        self.assertEqual(retval, True)
        # check that jars are no longer active
        self.assertEqual(sip1a.jar_set.filter(is_active=True).count(), 12)
        # check status of picklist
        self.assertEqual(picklist.status, PickList.PROCESSED)
        # check status of order
        self.assertEqual(self.order.status, Order.DELIVERED)
        # process it again
        # (should fail as status should have changed)
        retval2 = process_picklist(picklist)
        self.assertEqual(retval2, False)

    # FIXME: check cancel_picklist
    def test_cancel_picklist(self):
        # confirm both jars are marked available and active
        sip1a = Product.active.get(slug='sip-1-a')
        self.assertEqual(sip1a.jar_set.filter(is_active=True).count(), 14)
        self.assertEqual(sip1a.jar_set.filter(is_available=True).count(), 14)
        # generate valid picklist from order #1
        picklist = create_picklist(self.order)
        # confirm jars are unavailable
        self.assertEqual(sip1a.jar_set.filter(is_available=True).count(), 12)
        retval = cancel_picklist(picklist)
        self.assertEqual(retval, True)
        # check that jars are available again
        self.assertEqual(sip1a.jar_set.filter(is_available=True).count(), 14)
        # check status of picklist
        self.assertEqual(picklist.status, PickList.CANCELLED)
        # check status of order
        self.assertEqual(self.order.status, Order.SUBMITTED)
