from decimal import Decimal
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import Ingredient, IngredientItem, Parent, Recipe, SIPParent, Batch, Sample, Product, ProductReview
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def login_as_admin(self, url):
        userdict = {'username': 'admin',
                    'password': 'pbkdf2_sha256$10000$dMAdIm5LrBkt$gS8TSnpYq7J/YEbEeQ5AMr6AHOz/RHtHIapWHKjSHwM=',
                    'email': 'admin@example.com',
                    'is_superuser': True,
                    'is_staff': True,
                    }
        admin_user, created = User.objects.get_or_create(username=userdict['username'], defaults=userdict)
        self.selenium.get(self.live_server_url + url)
        username_field = self.selenium.find_element_by_name('username')
        username_field.send_keys(userdict['username'])
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
    fixtures = ['meadery']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        self.login_as_admin(reverse('admin:meadery_ingredient_add'))
        # Set boring fields.
        fields = {'name': 'Test Honey',
                  'appellation': '(None)',
                  'sg': '1.422',
                  'sh': '0.57',
                  'cpu': '7.95'}
        for key, value in fields.items():
            field = self.selenium.find_element_by_name(key)
            field.clear()
            field.send_keys(value)
        # JMT: is checking just the 'Sugar' case adequate?
        self.pick_option('type', 'Sugar')
        # Try saving with bad subtype values.
        bad_subtypes = ['Water', 'Spice', 'Dry']
        for subtype in bad_subtypes:
            self.pick_option('subtype', subtype)
            self.selenium.find_element_by_name('_save').click()
            self.assertIn('Ingredient type and subtype must match.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with bad state values.
        self.pick_option('subtype', 'Honey')
        bad_states = ['Liquid', 'Other']
        for state in bad_states:
            self.pick_option('state', state)
            self.selenium.find_element_by_name('_save').click()
            self.assertIn('Ingredient state does not match type.', self.selenium.find_element_by_tag_name('body').text)
        # Try saving with 'Sugar | Honey | Solid': succeed
        self.pick_option('state', 'Solid')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The ingredient "%s" was added successfully.' % fields['name'], self.selenium.find_element_by_tag_name('body').text)

    def test_modify(self):
        name = Ingredient.objects.get(pk=1).name
        self.login_as_admin(reverse('admin:meadery_ingredient_change', args=(1,)))
        sh_field = self.selenium.find_element_by_name('sh')
        sh_field.clear()
        sh_field.send_keys('1.00')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The ingredient "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)

    def test_delete(self):
        name = Ingredient.objects.get(pk=1).name
        self.login_as_admin(reverse('admin:meadery_ingredient_delete', args=(1,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        # Yes, we are sure!
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # JMT: I need to check that this actually succeeded
        self.assertIn('The ingredient "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)


class IngredientItemTestCase(TestCase):
    """
    For now I am testing ingredient items from within recipes.
    """
    pass


class RecipeTestCase(SeleniumTestCase):
    """
    Recipes need tests, too.

    Adding recipes should be easy enough.
    -- especially since there is not yet any "recipe validation".

    Deleting recipes should also be easy enough.
    -- all ingredient items should be deleted, too.

    Changing recipes should be easy too!

    What about admin actions?  Creating a batch from a recipe?
    """
    fixtures = ['meadery']

    def test_add(self):
        pass

    def test_delete(self):
        name = Recipe.objects.get(pk=3).name
        self.login_as_admin(reverse('admin:meadery_recipe_delete', args=(3,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        # Yes, we are sure!
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('The recipe "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)

    def test_modify(self):
        pass

    def test_create_batch_from_recipe(self):
        pass
