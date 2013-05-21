from decimal import Decimal
from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from models import Ingredient, IngredientItem, Parent, Recipe, SIPParent, Batch, Sample, Product, ProductReview
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def login_as_admin(self):
        self.selenium.get(self.live_server_url + '/admin/')
        username_field = self.selenium.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.selenium.find_element_by_name('password')
        password_field.send_keys('passw0rd')
        password_field.send_keys(Keys.RETURN)

    def pick_option(self, name, text):
        for option in self.selenium.find_element_by_name(name).find_elements_by_tag_name('option'):
            if option.text == text:
                option.click()


class ViewTest(TestCase):
    """
    One test for each view in urls.py
    """

    # JMT: currently testing only for success not for content
    fixtures = ['meadery']

    def test_meadery_home(self):
        response = self.client.get(reverse('meadery_home'))
        self.assertEqual(response.status_code, 200)

    def test_meadery_category(self):
        data = Product.active.order_by().values_list('category').distinct('category')[0][0]
        kwargs = {}
        kwargs['category_value'] = data
        response = self.client.get(reverse('meadery_category', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

    def test_meadery_product(self):
        data = Product.active.order_by().values_list('slug')[0][0]
        kwargs = {}
        kwargs['product_slug'] = data
        response = self.client.get(reverse('meadery_product', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

    def test_product_add_review(self):
        # JMT: not exactly sure how to do this...
        pass


class IngredientTestCase(SeleniumTestCase):
    """
    This class tests ingredients.  Adding, deleting, whatever else.
    """
    fixtures = ['meadery', 'auth']

    def setUp(self):
        self.login_as_admin()

    def tearDown(self):
        pass

    def test_add(self):
        self.selenium.get(self.live_server_url + '/admin/meadery/ingredient/add/')
        # Set boring fields.
        name_field = self.selenium.find_element_by_name('name')
        name_field.send_keys('Test Honey')
        appellation_field = self.selenium.find_element_by_name('appellation')
        appellation_field.send_keys('(None)')
        sg_field = self.selenium.find_element_by_name('sg')
        sg_field.clear()
        sg_field.send_keys('1.422')
        sh_field = self.selenium.find_element_by_name('sh')
        sh_field.clear()
        sh_field.send_keys('0.57')
        cpu_field = self.selenium.find_element_by_name('cpu')
        cpu_field.clear()
        cpu_field.send_keys('7.95')
        # JMT: is checking just the 'Sugar' case adequate?
        self.pick_option('type', 'Sugar')
        # Try saving with 'Sugar | Water': fail
        self.pick_option('subtype', 'Water')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('Ingredient type and subtype must match.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with 'Sugar | Spice': fail
        self.pick_option('subtype', 'Spice')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('Ingredient type and subtype must match.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with 'Sugar | Dry': fail
        self.pick_option('subtype', 'Dry')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('Ingredient type and subtype must match.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with 'Sugar | Honey | Liquid': fail
        self.pick_option('subtype', 'Honey')
        self.pick_option('state', 'Liquid')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('Ingredient state does not match type.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with 'Sugar | Honey | Other': fail
        self.pick_option('state', 'Other')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('Ingredient state does not match type.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with 'Sugar | Honey | Solid': succeed
        self.pick_option('state', 'Solid')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The ingredient "Test Honey" was added successfully.', self.selenium.find_element_by_tag_name('body').text)

    # def test_modify(self):
    #     # JMT: this also involves accessing the form.  eek.
    #     pass

    # def test_delete(self):
    #     # JMT: deleting an ingredient in a recipe should not remove the recipe
    #     pass


class IngredientItemTestCase(TestCase):
    """
    This class tests ingredient items.

    How do we do this?  Ingredient items are internal to recipes.
    Should I test them inside recipes?

    """
    pass
