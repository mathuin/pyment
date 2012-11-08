from django.test import TestCase, Client
from django.core import urlresolvers
import httplib
from django.contrib.auth import SESSION_KEY
from catalog.models import Category, Product
from pyment import views

class NewUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        logged_in = self.client.session.has_key(SESSION_KEY)
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
    def test_delete_all(self):
        for p in Product.objects.all():
            p.delete()
        # check that the data really was deleted
        self.assertEqual(Product.objects.all().count(),0)
    
    def test_products_exist(self):
        self.assertTrue(Product.objects.all().count() > 0)
        
class ProductTestCase(TestCase):
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
        
class CategoryTestCase(TestCase):
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
    

