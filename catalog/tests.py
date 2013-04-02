from django.test import TestCase, Client
from django.core import urlresolvers
import httplib
from django.contrib.auth import SESSION_KEY
from catalog.models import Category, Product
from inventory.models import Jar


class NewUserTestCase(TestCase):
    fixtures = ['catalog']

    def setUp(self):
        self.client = Client()
        logged_in = SESSION_KEY in self.client.session
        self.assertFalse(logged_in)

    def test_view_homepage(self):
        home_url = urlresolvers.reverse('catalog_home')
        response = self.client.get(home_url)
        # check that we did get a response
        self.failUnless(response)
        # check that status code of response was success
        self.assertEqual(response.status_code, httplib.OK)

    def test_view_category(self):
        category = Category.active.all()[0]
        category_url = category.get_absolute_url()
        # get the template_name arg from URL entry
        url_entry = urlresolvers.resolve(category_url)
        template_name = url_entry[2]['template_name']
        # test loading of category page
        response = self.client.get(category_url)
        # test that we got a response
        self.failUnless(response)
        # test that the HTTP status code was "OK"
        self.assertEqual(response.status_code, httplib.OK)
        # test that we used the category.html template in response
        self.assertTemplateUsed(response, template_name)
        # test that category page contains category information
        self.assertContains(response, category.name)
        self.assertContains(response, category.description)

    def test_view_product(self):
        """ test product view loads """
        product = Product.active.all()[0]
        product_url = product.get_absolute_url()
        url_entry = urlresolvers.resolve(product_url)
        template_name = url_entry[2]['template_name']
        response = self.client.get(product_url)
        self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, product.name)
        self.assertContains(response, product.description)


class DeleteExistTestCase(TestCase):
    fixtures = ['catalog']

    def test_delete_all(self):
        for p in Product.objects.all():
            p.delete()
        # check that the data really was deleted
        self.assertEqual(Product.objects.all().count(), 0)

    def test_products_exist(self):
        self.assertTrue(Product.objects.all().count() > 0)


class ProductTestCase(TestCase):
    fixtures = ['catalog', 'inventory']

    def setUp(self):
        self.product = Product.active.all()[0]
        self.client = Client()

    def test_permalink(self):
        url = self.product.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)

    def test_unicode(self):
        self.assertEqual(self.product.__unicode__(), self.product.name)

    def test_jars_in_stock(self):
        # one product with two jars that are available and true (returns 2)
        sip1a = Product.active.get(slug='sip-1-a')
        self.assertEqual(sip1a.jars_in_stock().count(), 2)
        # one product with no jars (0)
        sip1b = Product.active.get(slug='sip-1-b')
        self.assertEqual(sip1b.jars_in_stock().count(), 0)
        # one product with one jar that is available but not true (0)
        sip1c = Product.active.get(slug='sip-1-c')
        self.assertEqual(sip1c.jars_in_stock().count(), 0)

    def test_first_available(self):
        # returns first jar (see sip1a in test_jars_in_stock)
        sip1a = Product.active.get(slug='sip-1-a')
        jar1a2 = Jar.objects.get(slug='sip-1-a2')
        self.assertEqual(sip1a.first_available(), jar1a2)
        # returns None (see sip1b in test_jars_in_stock)
        sip1b = Product.active.get(slug='sip-1-b')
        self.assertEqual(sip1b.first_available(), None)
        # returns None (see sip1c in test_jars_in_stock)
        sip1c = Product.active.get(slug='sip-1-c')
        self.assertEqual(sip1c.first_available(), None)

    def test_abv(self):
        # check for valid values
        sip1a = Product.active.get(slug='sip-1-a')
        self.assertEqual(sip1a.abv, '6.27')
        # check for equal SGs
        sip1b = Product.active.get(slug='sip-1-b')
        self.assertEqual(sip1b.abv, '---')
        # check for one SG being zero
        sip1c = Product.active.get(slug='sip-1-c')
        self.assertEqual(sip1c.abv, '---')


class CategoryTestCase(TestCase):
    fixtures = ['catalog']

    def setUp(self):
        self.category = Category.active.all()[0]
        self.client = Client()

    def test_permalink(self):
        url = self.category.get_absolute_url()
        response = self.client.get(url)
        self.failUnless(response)
        self.failUnlessEqual(response.status_code, httplib.OK)

    def test_unicode(self):
        self.assertEqual(self.category.__unicode__(), self.category.name)

    def test_instock(self):
        # FIXME: needs fixtures
        # one category with one product that is inactive wtih one jar (false)
        # one category with one product that is active with no jars (false)
        # one category with one product that is active wtih one jar (true)
        return True

# No product review tests?!
