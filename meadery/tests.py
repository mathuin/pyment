from decimal import Decimal
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import Ingredient, IngredientItem, Parent, Recipe, SIPParent, Batch, Sample, Product, ProductReview
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

# JMT: There's a whole lot of trusting-the-admin-site-output here.
# Nearly all these tests are testing for *success*, not for *accuracy*.


class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(1)
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
    fixtures = ['meadery']

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
        ingredient = Ingredient.objects.all()[0]
        pk = ingredient.pk
        name = ingredient.name
        self.login_as_admin(reverse('admin:meadery_ingredient_change', args=(pk,)))
        sh_field = self.selenium.find_element_by_name('sh')
        sh_field.clear()
        sh_field.send_keys('1.00')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The ingredient "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)

    def test_delete(self):
        ingredient = Ingredient.objects.all()[0]
        pk = ingredient.pk
        name = ingredient.name
        self.login_as_admin(reverse('admin:meadery_ingredient_delete', args=(pk,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('The ingredient "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)


class IngredientItemTestCase(TestCase):
    """
    For now I am testing ingredient items from within recipes.
    """
    pass


class RecipeTestCase(SeleniumTestCase):
    fixtures = ['meadery']

    def test_add(self):
        # JMT: eventually test for 'bad recipes', whatever that means
        # ... missing yeast?  missing water?  missing sugar?
        self.login_as_admin(reverse('admin:meadery_recipe_add'))
        # Set boring fields.
        fields = {'title': 'Test Recipe',
                  'description': 'Test description!'}
        for key, value in fields.items():
            field = self.selenium.find_element_by_name(key)
            field.clear()
            field.send_keys(value)
        # Set ingredients.
        ingredients = [['Local Honey', '4.540', '70'],
                       ['Local Water', '9.725', '140'],
                       ['Local Water', '9.725', '70'],
                       ['Red Star Champagne Yeast', '1', '100']]
        for index, ingredient in enumerate(ingredients):
            name, amount, temp = ingredient
            idhead = 'ingredientitem_set-%d' % index
            step = 0
            found = False
            while step < 10:
                try:
                    div = self.selenium.find_element_by_id(idhead)
                    found = True
                    break
                except NoSuchElementException:
                    step = step + 1
                    self.selenium.find_element_by_link_text('Add another Ingredient Item').click()
            self.assertTrue(found)
            self.pick_option('%s-ingredient' % idhead, name)
            amount_field = self.selenium.find_element_by_name('%s-amount' % idhead)
            amount_field.clear()
            amount_field.send_keys(amount)
            temp_field = self.selenium.find_element_by_name('%s-temp' % idhead)
            temp_field.clear()
            temp_field.send_keys(temp)
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The recipe "%s" was added successfully.' % fields['title'], self.selenium.find_element_by_tag_name('body').text)

    def test_delete(self):
        recipe = Recipe.objects.all()[0]
        pk = recipe.pk
        name = recipe.name
        self.login_as_admin(reverse('admin:meadery_recipe_delete', args=(pk,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        # Yes, we are sure!
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('The recipe "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)

    def test_modify(self):
        recipe = Recipe.objects.all()[0]
        pk = recipe.pk
        name = recipe.name
        self.login_as_admin(reverse('admin:meadery_recipe_change', args=(pk,)))
        description_field = self.selenium.find_element_by_name('description')
        description_field.clear()
        description_field.send_keys('New Description')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The recipe "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)

    def test_create_batch_from_recipe(self):
        recipe = Recipe.objects.all()[0]
        pk = recipe.pk
        name = recipe.name
        self.login_as_admin(reverse('admin:meadery_recipe_change', args=(pk,)))
        self.selenium.find_element_by_link_text('Create batch from recipe').click()
        self.assertIn('One batch was created', self.selenium.find_element_by_tag_name('body').text)


class BatchTestCase(SeleniumTestCase):
    pass


class SampleTestCase(SeleniumTestCase):
    pass


class ProductTestCase(SeleniumTestCase):
    pass


class ProductReviewTestCase(SeleniumTestCase):
    """
    I do not know if I'm going to bother with this.
    """
    pass
