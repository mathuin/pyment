from decimal import Decimal
from django.db.models import Count
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import Ingredient, IngredientItem, Parent, Recipe, SIPParent, Batch, Sample, Product, ProductReview
from inventory.models import Jar
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class SeleniumTestCase(LiveServerTestCase):
    def go(self, url):
        self.selenium.get(self.live_server_url + url)

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(1)
        super(SeleniumTestCase, cls).setUpClass()

    def setUp(self):
        userdict = {'username': 'admin',
                    'password': 'pbkdf2_sha256$10000$dMAdIm5LrBkt$gS8TSnpYq7J/YEbEeQ5AMr6AHOz/RHtHIapWHKjSHwM=',
                    'email': 'admin@example.com',
                    'is_superuser': True,
                    'is_staff': True, }
        admin_user, created = User.objects.get_or_create(username=userdict['username'], defaults=userdict)
        self.go(reverse('admin:index'))
        username_field = self.selenium.find_element_by_name('username')
        username_field.send_keys(userdict['username'])
        password_field = self.selenium.find_element_by_name('password')
        password_field.send_keys('passw0rd')
        password_field.send_keys(Keys.RETURN)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def pick_option(self, name, text):
        for option in self.selenium.find_element_by_name(name).find_elements_by_tag_name('option'):
            if option.text == text:
                option.click()

    def populate_object(self, fields={}, ingredients=[]):
        for key, value in fields.items():
            field = self.selenium.find_element_by_name(key)
            field.clear()
            field.send_keys(value)
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


class ViewTest(TestCase):
    fixtures = ['meadery']

    def test_meadery_home(self):
        response = self.client.get(reverse('meadery_home'))
        self.assertEqual(response.status_code, 200)

    def test_meadery_category(self):
        try:
            data = Product.active.order_by().values_list('category').distinct('category')[0][0]
        except IndexError:
            self.fail('No active products found!')
        kwargs = {}
        kwargs['category_value'] = data
        response = self.client.get(reverse('meadery_category', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

    def test_meadery_product(self):
        try:
            data = Product.active.order_by().values_list('slug')[0][0]
        except IndexError:
            self.fail('No active products found!')
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
        fields = {'name': 'Test Honey',
                  'appellation': '(None)',
                  'sg': '1.422',
                  'sh': '0.57',
                  'cpu': '7.95'}
        # Ingredient does not yet exist in database.
        self.assertFalse((Ingredient.objects.filter(name=fields['name']).exists()))
        self.go(reverse('admin:meadery_ingredient_add'))
        self.populate_object(fields)
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
        # Ingredient should now exist in database.
        self.assertTrue(Ingredient.objects.filter(name=fields['name']).exists())

    def test_modify(self):
        try:
            ingredient = Ingredient.objects.all()[0]
        except IndexError:
            self.fail('No ingredients found!')
        pk = ingredient.pk
        name = ingredient.name
        old_cpu = ingredient.cpu
        new_cpu = old_cpu + Decimal('1.00')
        self.go(reverse('admin:meadery_ingredient_change', args=(pk,)))
        self.populate_object({'cpu': str(new_cpu)})
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The ingredient "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        ingredient = Ingredient.objects.get(pk=pk)
        self.assertNotEqual(old_cpu, ingredient.cpu)
        self.assertEqual(new_cpu, ingredient.cpu)

    def test_delete(self):
        try:
            ingredient = Ingredient.objects.all()[0]
        except IndexError:
            self.fail('No ingredients found!')
        pk = ingredient.pk
        name = ingredient.name
        self.go(reverse('admin:meadery_ingredient_delete', args=(pk,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('The ingredient "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        self.assertFalse(Ingredient.objects.filter(pk=pk).exists())


class IngredientItemTestCase(TestCase):
    """
    For now I am testing ingredient items from within recipes.
    """
    pass


class RecipeTestCase(SeleniumTestCase):
    fixtures = ['meadery']

    def test_add(self):
        # JMT: in the far future, recipes may also require:
        #  - the final temperature of the mixture be in the yeast friendly range
        #  - the final volume of the mixture be no bigger than the bucket/carboy it goes into
        fields = {'title': 'Test Recipe',
                  'description': 'Test description!'}
        all_ingredients = [['Local Honey', '4.540', '70'],
                           ['Local Water', '9.725', '140'],
                           ['Local Water', '9.725', '70'],
                           ['Red Star Champagne Yeast', '1', '100']]
        ingindex_output = [[[0, 1, 2], 'At least one yeast is required'],
                           [[1, 2, 3], 'At least one sugar source is required'],
                           [[0, 1, 3], 'At least two solvents with different temperatures are required'],
                           [[0, 1, 1, 3], 'At least two solvents with different temperatures are required'],
                           [[0, 1, 2, 3], 'was added successfully']]
        for test in ingindex_output:
            ingindex, output = test
            ingredients = [all_ingredients[x] for x in ingindex]
            self.assertFalse(Recipe.objects.filter(title=fields['title']).exists())
            self.go(reverse('admin:meadery_recipe_add'))
            self.populate_object(fields, ingredients)
            self.selenium.find_element_by_name('_save').click()
            self.assertIn(output, self.selenium.find_element_by_tag_name('body').text)
            if output is 'was added successfully':
                self.assertTrue(Recipe.objects.filter(title=fields['title']).exists())
            else:
                self.assertFalse(Recipe.objects.filter(title=fields['title']).exists())

    def test_modify(self):
        try:
            recipe = Recipe.objects.all()[0]
        except IndexError:
            self.fail('No recipe found!')
        pk = recipe.pk
        name = recipe.name
        old_description = recipe.description
        new_description = old_description + ' changed'
        self.go(reverse('admin:meadery_recipe_change', args=(pk,)))
        self.populate_object({'description': new_description})
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The recipe "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        recipe = Recipe.objects.get(pk=pk)
        self.assertNotEqual(old_description, recipe.description)
        self.assertEqual(new_description, recipe.description)

    def test_delete(self):
        try:
            recipe = Recipe.objects.all()[0]
        except IndexError:
            self.fail('No recipe found!')
        pk = recipe.pk
        name = recipe.name
        self.go(reverse('admin:meadery_recipe_delete', args=(pk,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        # Yes, we are sure!
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('The recipe "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        self.assertFalse(Recipe.objects.filter(pk=pk).exists())

    def test_category(self):
        fields = {'title': 'Test Recipe',
                  'description': 'Test description'}
        dry_ingredients = [['Local Honey', '4.540', '70'],
                           ['Local Water', '9.725', '140'],
                           ['Local Water', '9.725', '70'],
                           ['Red Star Champagne Yeast', '1', '100']]
        cyser_ingredients = [['Local Honey', '4.540', '70'],
                             ['Apple Juice', '9.725', '140'],
                             ['Apple Juice', '9.725', '70'],
                             ['Red Star Champagne Yeast', '1', '100']]
        melomel_ingredients = [['Local Honey', '4.540', '70'],
                               ['Local Water', '9.725', '140'],
                               ['Local Water', '9.725', '70'],
                               ['Freeze-Dried Blueberry Powder', '0.238', '100'],
                               ['Red Star Champagne Yeast', '1', '100']]
        metheglin_ingredients = [['Local Honey', '4.540', '70'],
                                 ['Local Water', '9.725', '140'],
                                 ['Local Water', '9.725', '70'],
                                 ['Cinnamon Sticks', '10', '100'],
                                 ['Red Star Champagne Yeast', '1', '100']]
        open_ingredients = [['Local Honey', '4.540', '70'],
                            ['Apple Juice', '9.725', '140'],
                            ['Apple Juice', '9.725', '70'],
                            ['Cinnamon Sticks', '10', '100'],
                            ['Red Star Champagne Yeast', '1', '100']]
        tests = [[dry_ingredients, Parent.TRADITIONAL_DRY],
                 [cyser_ingredients, Parent.MELOMEL_CYSER],
                 [melomel_ingredients, Parent.MELOMEL_OTHER],
                 [metheglin_ingredients, Parent.OTHER_METHEGLIN],
                 [open_ingredients, Parent.OTHER_OPEN_CATEGORY], ]
        for test in tests:
            ingredients, category = test
            self.assertFalse(Recipe.objects.filter(title=fields['title']).exists())
            self.go(reverse('admin:meadery_recipe_add'))
            self.populate_object(fields, ingredients)
            self.selenium.find_element_by_name('_save').click()
            self.assertTrue(Recipe.objects.filter(title=fields['title']).exists())
            self.assertEqual(Recipe.objects.get(title=fields['title']).category, category)
            Recipe.objects.filter(title=fields['title']).delete()

    def test_appellation(self):
        fields = {'title': 'Test Recipe',
                  'description': 'Test description'}
        oregon_ingredients = [['Local Honey', '4.540', '70'],
                              ['Local Water', '9.725', '140'],
                              ['Local Water', '9.725', '70'],
                              ['Red Star Champagne Yeast', '1', '100']]
        none_ingredients = [['Scary Honey', '4.540', '70'],
                            ['Local Water', '9.725', '140'],
                            ['Local Water', '9.725', '70'],
                            ['Red Star Champagne Yeast', '1', '100']]
        tests = [[oregon_ingredients, 'Oregon'],
                 [none_ingredients, None], ]
        for test in tests:
            ingredients, appellation = test
            self.assertFalse(Recipe.objects.filter(title=fields['title']).exists())
            self.go(reverse('admin:meadery_recipe_add'))
            self.populate_object(fields, ingredients)
            self.selenium.find_element_by_name('_save').click()
            self.assertTrue(Recipe.objects.filter(title=fields['title']).exists())
            self.assertEqual(Recipe.objects.get(title=fields['title']).appellation, appellation)
            Recipe.objects.filter(title=fields['title']).delete()

    def test_natural(self):
        fields = {'title': 'Test Recipe',
                  'description': 'Test description'}
        true_ingredients = [['Local Honey', '4.540', '70'],
                            ['Local Water', '9.725', '140'],
                            ['Local Water', '9.725', '70'],
                            ['Red Star Champagne Yeast', '1', '100']]
        false_ingredients = [['Local Honey', '4.540', '70'],
                             ['Tap Water', '9.725', '140'],
                             ['Tap Water', '9.725', '70'],
                             ['Red Star Champagne Yeast', '1', '100']]
        tests = [[true_ingredients, True],
                 [false_ingredients, False], ]
        for test in tests:
            ingredients, all_natural = test
            self.assertFalse(Recipe.objects.filter(title=fields['title']).exists())
            self.go(reverse('admin:meadery_recipe_add'))
            self.populate_object(fields, ingredients)
            self.selenium.find_element_by_name('_save').click()
            self.assertTrue(Recipe.objects.filter(title=fields['title']).exists())
            self.assertEqual(Recipe.objects.get(title=fields['title']).all_natural, all_natural)
            Recipe.objects.filter(title=fields['title']).delete()

    def test_create_batch_from_recipe(self):
        try:
            recipe = Recipe.objects.all()[0]
        except IndexError:
            self.fail('No recipe found!')
        pk = recipe.pk
        name = recipe.name
        self.go(reverse('admin:meadery_recipe_change', args=(pk,)))
        old_batch_count = Batch.objects.count()
        self.selenium.find_element_by_link_text('Create batch from recipe').click()
        self.assertIn('One batch was created!', self.selenium.find_element_by_tag_name('body').text)
        new_batch_count = Batch.objects.count()
        self.assertEqual(new_batch_count, old_batch_count + 1)


class BatchTestCase(SeleniumTestCase):
    fixtures = ['meadery']

    def test_add(self):
        # JMT: in the far future, batchs may also require:
        #  - the final temperature of the mixture be in the yeast friendly range
        #  - the final volume of the mixture be no bigger than the bucket/carboy it goes into
        fields = {'title': 'Test Batch',
                  'description': 'Test description!',
                  'brewname': 'SIP 99',
                  'batchletter': 'A',
                  'event': 'Christmas',
                  'jars': '0'}
        all_ingredients = [['Local Honey', '4.540', '70'],
                           ['Local Water', '9.725', '140'],
                           ['Local Water', '9.725', '70'],
                           ['Red Star Champagne Yeast', '1', '100']]
        ingindex_output = [[[0, 1, 2], 'At least one yeast is required.'],
                           [[1, 2, 3], 'At least one sugar source is required.'],
                           [[0, 1, 3], 'At least two solvents with different temperatures are required.'],
                           [[0, 1, 1, 3], 'At least two solvents with different temperatures are required.'],
                           [[0, 1, 2, 3], 'was added successfully']]
        for test in ingindex_output:
            ingindex, output = test
            ingredients = [all_ingredients[x] for x in ingindex]
            self.assertFalse(Batch.objects.filter(title=fields['title']).exists())
            self.go(reverse('admin:meadery_batch_add'))
            self.populate_object(fields, ingredients)
            self.selenium.find_element_by_name('_save').click()
            self.assertIn(output, self.selenium.find_element_by_tag_name('body').text)
            if output is 'was added successfully':
                self.assertTrue(Batch.objects.filter(title=fields['title']).exists())
            else:
                self.assertFalse(Batch.objects.filter(title=fields['title']).exists())

    def test_modify(self):
        try:
            batch = Batch.objects.all()[0]
        except IndexError:
            self.fail('No batch found!')
        pk = batch.pk
        name = batch.name
        old_description = batch.description
        new_description = old_description + ' changed'
        self.go(reverse('admin:meadery_batch_change', args=(pk,)))
        self.populate_object({'description': new_description})
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The batch "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        batch = Batch.objects.get(pk=pk)
        self.assertNotEqual(old_description, batch.description)
        self.assertEqual(new_description, batch.description)

    def test_delete(self):
        batches = Batch.objects.annotate(num_samples=Count('sample'))
        try:
            batch_from_scratch_without_samples = batches.filter(recipe__isnull=True, num_samples=0)[0]
        except IndexError:
            self.fail('There is no batch from scratch without samples in the fixture!')
        try:
            batch_from_scratch_with_samples = batches.filter(recipe__isnull=True, num_samples__gt=0)[0]
        except IndexError:
            self.fail('There is no batch from scratch with samples in the fixture!')
        try:
            batch_from_recipe_without_samples = batches.filter(recipe__isnull=False, num_samples=0)[0]
        except IndexError:
            self.fail('There is no batch from a recipe without samples in the fixture!')
        try:
            batch_from_recipe_with_samples = batches.filter(recipe__isnull=False, num_samples__gt=0)[0]
        except IndexError:
            self.fail('There is no batch from a recipe with samples in the fixture!')
        for batch in [batch_from_scratch_without_samples, batch_from_scratch_with_samples, batch_from_recipe_without_samples, batch_from_recipe_with_samples]:
            pk = batch.pk
            name = batch.name
            old_sample_count = Sample.objects.count()
            batch_sample_count = Sample.objects.filter(batch=batch).count()
            self.go(reverse('admin:meadery_batch_delete', args=(pk,)))
            body = self.selenium.find_element_by_tag_name('body')
            self.assertIn('Are you sure?', body.text)
            self.assertIn('All of the following related items will be deleted', body.text)
            self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
            self.assertIn('The batch "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
            new_sample_count = Sample.objects.count()
            self.assertEqual(new_sample_count, old_sample_count - batch_sample_count)
            self.assertFalse(Batch.objects.filter(pk=pk).exists())

    def test_create_recipe_from_batch(self):
        try:
            batch = Batch.objects.all()[0]
        except IndexError:
            self.fail('No batch found!')
        pk = batch.pk
        old_recipe_count = Recipe.objects.count()
        self.go(reverse('admin:meadery_batch_change', args=(pk,)))
        self.selenium.find_element_by_link_text('Create recipe from batch').click()
        self.assertIn('One recipe was created!', self.selenium.find_element_by_tag_name('body').text)
        new_recipe_count = Recipe.objects.count()
        self.assertEqual(new_recipe_count, old_recipe_count + 1)

    def test_create_product_from_batch(self):
        # First, remove all batches that have already been converted into products.
        batches = Batch.objects.annotate(num_samples=Count('sample'))
        for prod in Product.objects.all():
            batches = batches.exclude(brewname=prod.brewname, batchletter=prod.batchletter)
        # What's left is available for testing.
        try:
            batch_with = batches.filter(num_samples__gt=0)[0]
        except IndexError:
            self.fail('There is no unconverted batch with samples in the fixture!')
        try:
            batch_without = batches.filter(num_samples=0)[0]
        except IndexError:
            self.fail('There is no unconverted batch without samples in the fixture!')
        # Final test should fail because a batch cannot be turned into a product twice.
        samples_jars_output = [[True, 0, 'No product was created!'],
                               [False, 0, 'No product was created!'],
                               [False, 24, 'No product was created!'],
                               [True, 24, 'One product was created!'],
                               [True, 24, 'No product was created!'], ]
        for test in samples_jars_output:
            samples, jars, output = test
            batch = batch_with if samples else batch_without
            batch.jars = jars
            batch.save()
            pk = batch.pk
            old_product_count = Product.objects.count()
            self.go(reverse('admin:meadery_batch_change', args=(pk,)))
            self.selenium.find_element_by_link_text('Create product from batch').click()
            self.assertIn(output, self.selenium.find_element_by_tag_name('body').text)
            new_product_count = Product.objects.count()
            if output is 'One product was created!':
                self.assertTrue(Product.objects.filter(title=batch.title).exists())
                self.assertEqual(new_product_count, old_product_count + 1)
            else:
                self.assertEqual(new_product_count, old_product_count)

    def test_make_labels(self):
        # JMT: conventional wisdom on the internet says don't test file downloads
        pass


class SampleTestCase(SeleniumTestCase):
    fixtures = ['meadery']

    def test_add(self):
        fields = {'date': '2012-05-31',
                  'temp': '60',
                  'sg': '1.168',
                  'notes': 'Tastes great for a test!'}
        self.assertFalse(Sample.objects.filter(notes=fields['notes']).exists())
        self.go(reverse('admin:meadery_sample_add'))
        self.populate_object(fields)
        try:
            batch = Batch.objects.all()[0].name
        except IndexError:
            self.fail('No batch found!')
        self.pick_option('batch', batch)
        self.selenium.find_element_by_name('_save').click()
        body = self.selenium.find_element_by_tag_name('body')
        # Figuring out the middle is annoying.
        self.assertIn('The sample ', body.text)
        self.assertIn('was added successfully.', body.text)
        self.assertTrue(Sample.objects.filter(notes=fields['notes']).exists())

    def test_modify(self):
        # JMT: consider changing sg value and checking batch's abv
        try:
            sample = Sample.objects.all()[0]
        except IndexError:
            self.fail('No samples found!')
        pk = sample.pk
        name = sample.__unicode__()
        old_notes = sample.notes
        new_notes = old_notes + ' changed'
        self.go(reverse('admin:meadery_sample_change', args=(pk,)))
        self.populate_object({'notes': new_notes})
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The sample "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        sample = Sample.objects.get(pk=pk)
        self.assertNotEqual(old_notes, sample.notes)
        self.assertEqual(new_notes, sample.notes)

    def test_delete(self):
        try:
            sample = Sample.objects.all()[0]
        except IndexError:
            self.fail('No samples found!')
        pk = sample.pk
        name = sample.__unicode__()
        old_batch_count = Batch.objects.count()
        self.go(reverse('admin:meadery_sample_delete', args=(pk,)))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Are you sure?', body.text)
        self.assertIn('All of the following related items will be deleted', body.text)
        # Yes, we are sure!
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('The sample "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        new_batch_count = Batch.objects.count()
        self.assertEqual(old_batch_count, new_batch_count)
        self.assertFalse(Sample.objects.filter(pk=pk).exists())


class ProductTestCase(SeleniumTestCase):
    fixtures = ['meadery', 'inventory']

    def test_add(self):
        # Set boring fields.
        fields = {'title': 'Test Product',
                  'description': 'Test description!',
                  'brewname': 'SIP 99',
                  'batchletter': 'A',
                  'meta_keywords': 'bogus',
                  'meta_description': 'bogus',
                  'brewed_date': '2013-05-01',
                  'brewed_sg': '1.126',
                  'bottled_date': '2013-05-31',
                  'bottled_sg': '0.996',
                  'abv': '17.33'}
        self.assertFalse(Product.objects.filter(title=fields['title']).exists())
        self.go(reverse('admin:meadery_product_add'))
        self.populate_object(fields)
        self.pick_option('category', 'Dry Mead')
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The product "%s %s" was added successfully.' % (fields['brewname'], fields['batchletter']), self.selenium.find_element_by_tag_name('body').text)
        self.assertTrue(Product.objects.filter(title=fields['title']).exists())

    def test_modify(self):
        try:
            product = Product.objects.all()[0]
        except IndexError:
            self.fail('No products found!')
        pk = product.pk
        name = product.name
        old_description = product.description
        new_description = old_description + ' changed'
        self.go(reverse('admin:meadery_product_change', args=(pk,)))
        self.populate_object({'description': new_description})
        self.selenium.find_element_by_name('_save').click()
        self.assertIn('The product "%s" was changed successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        product = Product.objects.get(pk=pk)
        self.assertNotEqual(old_description, product.description)
        self.assertEqual(new_description, product.description)

    def test_delete(self):
        products = Product.objects.annotate(num_jars=Count('jar'))
        try:
            product_with = products.filter(num_jars__gt=0)[0]
        except IndexError:
            self.fail('No products with jars found!')
        try:
            product_without = products.filter(num_jars=0)[0]
        except IndexError:
            self.fail('No products without jars found!')
        for product in [product_with, product_without]:
            pk = product.pk
            name = product.name
            old_jar_count = Jar.objects.count()
            product_jar_count = Jar.objects.filter(product=product).count()
            self.go(reverse('admin:meadery_product_delete', args=(pk,)))
            body = self.selenium.find_element_by_tag_name('body')
            self.assertIn('Are you sure?', body.text)
            self.assertIn('All of the following related items will be deleted', body.text)
            self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
            self.assertIn('The product "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
            new_jar_count = Jar.objects.count()
            self.assertEqual(new_jar_count, old_jar_count - product_jar_count)
            self.assertFalse(Product.objects.filter(pk=pk).exists())


class ProductReviewTestCase(SeleniumTestCase):
    """
    I do not know if I'm going to bother with this.
    """
    pass
