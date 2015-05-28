from decimal import Decimal
from django.db.models import Count
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import Ingredient, Parent, Recipe, Batch, Sample, Product


# views.py
# show_category edge cases
# show_product post (add to cart)
# add_review (ugh, all cases)


class ViewTest(TestCase):
    fixtures = ['meadery', 'inventory']

    def setUp(self):
        self.product = Product.instock.all()[0]

    def test_meadery_home(self):
        response = self.client.get(reverse('meadery_home'))
        self.assertEqual(response.status_code, 200)

    def test_meadery_category(self):
        response = self.client.get(reverse('meadery_category', kwargs={'category_value': self.product.category}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.name)
        self.assertContains(response, 'In Stock: {0}'.format(self.product.jars_in_stock()))

    def test_meadery_product(self):
        response = self.client.get(reverse('meadery_product', kwargs={'product_slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test_product_add_review(self):
        # JMT: not exactly sure how to do this...
        pass


class IngredientItemTestCase(TestCase):
    """
    For now I am testing ingredient items from within recipes.
    """
    pass


class ProductReviewTestCase(TestCase):
    """
    I do not know if I'm going to bother with this.
    """
    pass


# test decorators
def admin_login(func):
    def _decorator(self, *args, **kwds):
        username = 'admin'
        rawpass = 'passw0rd'
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            admin_user = User.objects.create_superuser(username, email, rawpass)
            # need better test
            self.assertTrue(admin_user)
        logged_in = self.client.login(username=username, password=rawpass)
        self.assertTrue(logged_in)
        func(self, *args, **kwds)
        self.client.logout()
    return _decorator


class MeaderyTestCase(TestCase):
    fixtures = ['meadery']

    @classmethod
    def setUpClass(cls):
        cls.url = reverse('admin:index')

    def test_not_logged_in(self):
        # Get the ingredient page without logging in.
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        redirect_target = '{0}{1}?next={2}'.format('http://testserver',
                                                   reverse('admin:login'),
                                                   self.url)
        redirect_chain = [(redirect_target, 302)]
        self.assertEqual(response.redirect_chain, redirect_chain)


class IngredientTestCase(MeaderyTestCase):

    fields = {
        'name': 'Test Honey',
        'appellation': '(None)',
        'sg': '1.422',
        'sh': '0.57',
        'tolerance': '12',
        'cpu': '7.95',
    }

    def setUp(self):
        # super(MeaderyTestCase, self).setUp()
        self.url = reverse('admin:meadery_ingredient_changelist')
        self.fields = IngredientTestCase.fields


class IngredientAddTestCase(IngredientTestCase):

    def setUp(self):
        super(IngredientTestCase, self).setUp()
        self.url = reverse('admin:meadery_ingredient_add')

    def ingredient_exists(before, after):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                self.assertEqual(before, Ingredient.objects.filter(name=self.fields['name']).exists())
                func(self, *args, **kwds)
                self.assertEqual(after, Ingredient.objects.filter(name=self.fields['name']).exists())
            return _decorator
        return real_decorator

    def ingredient_add(mytype, subtype, state, respstr):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                fields = self.fields
                fields['type'] = mytype
                fields['subtype'] = subtype
                fields['state'] = state
                response = self.client.post(self.url, fields, follow=True)
                self.assertContains(response, respstr)
                func(self, *args, **kwds)
            return _decorator
        return real_decorator

    @ingredient_exists(False, False)
    @admin_login
    def test_no_post(self):
        # Send no POST data.
        response = self.client.post(self.url)
        self.assertContains(response, 'This field is required')
        # JMT: what do I put here?
        # self.assertFormError(response, XXX, YYY, 'This field is required.')

    @ingredient_exists(False, False)
    @admin_login
    @ingredient_add('2', '101', '1', 'Ingredient type and subtype must match.')  # Solvent is wrong type!
    def test_bad_post_wrongtype(self):
        pass

    @ingredient_exists(False, False)
    @admin_login
    @ingredient_add('1', '201', '1', 'Ingredient type and subtype must match.')  # Water is wrong subtype!
    def test_bad_post_wrongsubtype(self):
        pass

    @ingredient_exists(False, False)
    @ingredient_add
    @admin_login('1', '101', '2', 'Ingredient state does not match type.')  # Liquid is wrong state!
    def test_bad_post_wrongstate(self):
        pass

    @ingredient_exists(False, True)
    @admin_login
    @ingredient_add('1', '101', '1', 'The ingredient &quot;{0}&quot; was added successfully.'.format(IngredientTestCase.fields['name']))  # All good!
    def test_good_post(self):
        pass


class IngredientModifyTestCase(IngredientTestCase):
    def setUp(self):
        super(IngredientTestCase, self).setUp()
        self.ingredient = Ingredient.objects.all()[0]
        self.pk = self.ingredient.pk
        self.fields = {
            'name': self.ingredient.name,
            'appellation': self.ingredient.appellation,
            'sg': self.ingredient.sg,
            'sh': self.ingredient.sh,
            'cpu': self.ingredient.cpu,
            'type': self.ingredient.type,
            'subtype': self.ingredient.subtype,
            'state': self.ingredient.state,
            'tolerance': self.ingredient.tolerance,
        }
        self.url = reverse('admin:meadery_ingredient_change', args=(self.pk,))

    @admin_login
    def test_modify(self):
        old_cpu = self.ingredient.cpu
        new_cpu = old_cpu + Decimal('1.00')
        self.assertNotEqual(old_cpu, new_cpu)
        fields = self.fields
        fields['cpu'] = str(new_cpu)
        response = self.client.post(self.url, fields, follow=True)
        self.assertContains(response, 'The ingredient &quot;{0}&quot; was changed successfully.'.format(self.ingredient.name))
        ingredient = Ingredient.objects.get(pk=self.pk)
        self.assertNotEqual(old_cpu, ingredient.cpu)
        self.assertEqual(new_cpu, ingredient.cpu)


class IngredientDeleteTestCase(IngredientTestCase):

    def setUp(self):
        super(IngredientTestCase, self).setUp()
        self.ingredient = Ingredient.objects.all()[0]
        self.pk = self.ingredient.pk
        self.url = reverse('admin:meadery_ingredient_delete', args=(self.pk,))

    @admin_login
    def test_delete(self):
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, 'Are you sure?')
        # body = self.selenium.find_element_by_tag_name('body')
        # self.assertIn('Are you sure?', body.text)
        # self.assertIn('All of the following related items will be deleted', body.text)
        # self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # self.assertIn('The ingredient "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        # self.assertFalse(Ingredient.objects.filter(pk=pk).exists())


# JMT: in the far future, recipes may also require:
#  - the final temperature of the mixture be in the yeast friendly range
#  - the final volume of the mixture be no bigger than the bucket/carboy
class RecipeTestCase(MeaderyTestCase):

    fields = {
        'title': 'Test Recipe',
        'description': 'Test description!',
    }

    ingredients = [['Local Honey', '4.540', '70'],
                   ['Local Water', '9.725', '140'],
                   ['Local Water', '9.725', '70'],
                   ['Red Star Champagne Yeast', '1', '100']]

    def setUp(self):
        super(MeaderyTestCase, self).setUp()
        self.url = reverse('admin:meadery_recipe_changelist')

    @staticmethod
    def build_recipe(fields, ingredients):
        recipe = RecipeTestCase.fields
        recipe['ingredientitem_set-TOTAL_FORMS'] = len(ingredients)
        recipe['ingredientitem_set-INITIAL_FORMS'] = '0'
        recipe['ingredientitem_set-MIN_NUM_FORMS'] = '0'
        recipe['ingredientitem_set-MAX_NUM_FORMS'] = '1000'
        for index, ingredient in enumerate(ingredients):
            ing = Ingredient.objects.get(name=ingredient[0])
            key_head = 'ingredientitem_set-{0}'.format(index)
            recipe['{0}-id'.format(key_head)] = ''
            recipe['{0}-parent'.format(key_head)] = ''
            recipe['{0}-ingredient'.format(key_head)] = ing.pk
            recipe['{0}-amount'.format(key_head)] = ingredient[1]
            recipe['{0}-temp'.format(key_head)] = ingredient[2]
        key_head = 'ingredientitem_set-{0}'.format('__prefix__')
        recipe['{0}-id'.format(key_head)] = ''
        recipe['{0}-parent'.format(key_head)] = ''
        recipe['{0}-ingredient'.format(key_head)] = ''
        recipe['{0}-amount'.format(key_head)] = ''
        recipe['{0}-temp'.format(key_head)] = ''
        return recipe


class RecipeAddTestCase(RecipeTestCase):

    def setUp(self):
        super(RecipeTestCase, self).setUp()
        self.url = reverse('admin:meadery_recipe_add')
        self.recipe = RecipeTestCase.build_recipe(RecipeTestCase.fields, RecipeTestCase.ingredients)

    def recipe_exists(before, after):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                self.assertEqual(before, Recipe.objects.filter(title=self.recipe['title']).exists())
                func(self, *args, **kwds)
                self.assertEqual(after, Recipe.objects.filter(title=self.recipe['title']).exists())
            return _decorator
        return real_decorator

    def recipe_add(ings, respstr):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                recipe = RecipeTestCase.build_recipe(RecipeTestCase.fields, [RecipeTestCase.ingredients[x] for x in ings])
                func(self, *args, **kwds)
                response = self.client.post(self.url, recipe, follow=True)
                self.assertContains(response, respstr)
            return _decorator
        return real_decorator

    @recipe_exists(False, False)
    @admin_login
    @recipe_add([], 'At least one sugar source is required.')
    def test_bad_post_no_data(self):
        pass

    @recipe_exists(False, False)
    @admin_login
    @recipe_add([0, 1, 2], 'At least one yeast is required.')
    def test_bad_post_no_yeast(self):
        pass

    @recipe_exists(False, False)
    @admin_login
    @recipe_add([1, 2, 3], 'At least one sugar source is required.')
    def test_bad_post_no_sugar(self):
        pass

    @recipe_exists(False, False)
    @admin_login
    @recipe_add([0, 1, 3], 'At least two solvents with different temperatures are required.')
    def test_bad_post_not_enough_solvent(self):
        pass

    @recipe_exists(False, False)
    @admin_login
    @recipe_add([0, 1, 1, 3], 'At least two solvents with different temperatures are required.')
    def test_bad_post_solvents_same_temp(self):
        pass

    @recipe_exists(False, True)
    @admin_login
    @recipe_add([0, 1, 2, 3], 'The recipe &quot;{0}&quot; was added successfully.'.format(RecipeTestCase.fields['title']))
    def test_good_post(self):
        pass


class RecipeModifyTestCase(RecipeTestCase):
    def setUp(self):
        super(RecipeTestCase, self).setUp()
        self.recipe = Recipe.objects.all()[0]
        self.pk = self.recipe.pk
        self.url = reverse('admin:meadery_recipe_change', args=(self.pk,))

    @admin_login
    def test_modify(self):
        old_description = self.recipe.description
        new_description = old_description + '!!!'
        self.assertNotEqual(old_description, new_description)
        # JMT: this is ... excessive
        recipe = RecipeTestCase.build_recipe(RecipeTestCase.fields, RecipeTestCase.ingredients)
        recipe['description'] = new_description
        response = self.client.post(self.url, recipe, follow=True)
        self.assertContains(response, 'The recipe &quot;{0}&quot; was changed successfully.'.format(RecipeTestCase.fields['title']))
        recipe = Recipe.objects.get(pk=self.pk)
        self.assertNotEqual(old_description, recipe.description)
        self.assertEqual(new_description, recipe.description)

    @admin_login
    def test_create_batch_from_recipe(self):
        old_batch_count = Batch.objects.count()
        # JMT: figure out a better way to get this
        button_url = '{0}create_batch/'.format(self.url)
        response = self.client.get(button_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Creating a batch from recipe {0}:'.format(self.recipe.title))
        # Now that we're here, it's just another POST.
        fields = {
            'brewname': 'SIP 97',
            'batchletter': 'A',
            'event': 'Christmas',
            '_selected_action': self.recipe.title,
            'action': 'create_batch_from_recipe',
            'apply': 'Create batch',
        }
        response = self.client.post(button_url, fields, follow=True)
        self.assertEqual(response.status_code, 200)
        new_batch_count = Batch.objects.count()
        self.assertEqual(new_batch_count, old_batch_count + 1)


class RecipeDeleteTestCase(RecipeTestCase):

    def setUp(self):
        super(RecipeTestCase, self).setUp()
        self.recipe = Recipe.objects.all()[0]
        self.pk = self.recipe.pk
        self.url = reverse('admin:meadery_recipe_delete', args=(self.pk,))

    @admin_login
    def test_delete(self):
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, 'Are you sure?')
        # body = self.selenium.find_element_by_tag_name('body')
        # self.assertIn('Are you sure?', body.text)
        # self.assertIn('All of the following related items will be deleted', body.text)
        # self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # self.assertIn('The recipe "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        # self.assertFalse(Recipe.objects.filter(pk=pk).exists())


class RecipeMiscTestCase(RecipeTestCase):

    # categories
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

    # appellations
    oregon_ingredients = [['Local Honey', '4.540', '70'],
                          ['Local Water', '9.725', '140'],
                          ['Local Water', '9.725', '70'],
                          ['Red Star Champagne Yeast', '1', '100']]
    none_ingredients = [['Scary Honey', '4.540', '70'],
                        ['Local Water', '9.725', '140'],
                        ['Local Water', '9.725', '70'],
                        ['Red Star Champagne Yeast', '1', '100']]

    # naturalness
    true_ingredients = [['Local Honey', '4.540', '70'],
                        ['Local Water', '9.725', '140'],
                        ['Local Water', '9.725', '70'],
                        ['Red Star Champagne Yeast', '1', '100']]
    false_ingredients = [['Local Honey', '4.540', '70'],
                         ['Tap Water', '9.725', '140'],
                         ['Tap Water', '9.725', '70'],
                         ['Red Star Champagne Yeast', '1', '100']]

    def setUp(self):
        super(RecipeTestCase, self).setUp()
        self.recipe = Recipe.objects.all()[0]
        self.pk = self.recipe.pk
        self.url = reverse('admin:meadery_recipe_add')

    def recipe_add_category(inglist, category):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                func(self, *args, **kwds)
                recipe = RecipeTestCase.build_recipe(RecipeTestCase.fields, inglist)
                response = self.client.post(self.url, recipe, follow=True)
                self.assertTrue(response.return_code, 200)
                new_recipe = Recipe.objects.get(title=recipe['title'])
                self.assertEqual(new_recipe.category, category)
                # hopefully not necessary
                Recipe.objects.filter(title=recipe['title']).delete()
            return _decorator
        return real_decorator

    def recipe_add_appellation(inglist, appellation):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                func(self, *args, **kwds)
                recipe = RecipeTestCase.build_recipe(RecipeTestCase.fields, inglist)
                response = self.client.post(self.url, recipe, follow=True)
                self.assertTrue(response.return_code, 200)
                new_recipe = Recipe.objects.get(title=recipe['title'])
                self.assertEqual(new_recipe.appellation, appellation)
                # hopefully not necessary
                Recipe.objects.filter(title=recipe['title']).delete()
            return _decorator
        return real_decorator

    def recipe_add_natural(inglist, natural):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                func(self, *args, **kwds)
                recipe = RecipeTestCase.build_recipe(RecipeTestCase.fields, inglist)
                response = self.client.post(self.url, recipe, follow=True)
                self.assertTrue(response.return_code, 200)
                new_recipe = Recipe.objects.get(title=recipe['title'])
                self.assertEqual(new_recipe.all_natural, natural)
                # hopefully not necessary
                Recipe.objects.filter(title=recipe['title']).delete()
            return _decorator
        return real_decorator

    @admin_login
    @recipe_add_category(dry_ingredients, Parent.TRADITIONAL_DRY)
    def test_category_dry(self):
        pass

    @admin_login
    @recipe_add_category(cyser_ingredients, Parent.MELOMEL_CYSER)
    def test_category_cyser(self):
        pass

    @admin_login
    @recipe_add_category(melomel_ingredients, Parent.MELOMEL_OTHER)
    def test_category_melomel(self):
        pass

    @admin_login
    @recipe_add_category(metheglin_ingredients, Parent.OTHER_METHEGLIN)
    def test_category_metheglin(self):
        pass

    @admin_login
    @recipe_add_category(open_ingredients, Parent.OTHER_OPEN_CATEGORY)
    def test_category_open(self):
        pass

    @admin_login
    @recipe_add_appellation(oregon_ingredients, 'Oregon')
    def test_appellation_oregon(self):
        pass

    @admin_login
    @recipe_add_appellation(none_ingredients, None)
    def test_appellation_none(self):
        pass

    @admin_login
    @recipe_add_natural(true_ingredients, True)
    def test_natural_true(self):
        pass

    @admin_login
    @recipe_add_natural(false_ingredients, False)
    def test_natural_false(self):
        pass


class BatchTestCase(MeaderyTestCase):

    # JMT: in the far future, batchs may also require:
    #  - the final temperature of the mixture be in the yeast friendly range
    #  - the final volume of the mixture be no bigger than the bucket/carboy it goes into

    fields = {
        'brewname': 'SIP 99',
        'batchletter': 'A',
        'event': 'Christmas',
        'title': 'Test Batch',
        'description': 'Test description!',
        'jars': '0'
    }

    ingredients = [['Local Honey', '4.540', '70'],
                   ['Local Water', '9.725', '140'],
                   ['Local Water', '9.725', '70'],
                   ['Red Star Champagne Yeast', '1', '100']]

    samples = []

    def setUp(self):
        super(MeaderyTestCase, self).setUp()
        self.url = reverse('admin:meadery_batch_changelist')

    @staticmethod
    def build_batch(fields, ingredients, samples):
        batch = {}
        for key, value in BatchTestCase.fields.items():
            batch[key] = value
        batch['ingredientitem_set-TOTAL_FORMS'] = len(ingredients)
        batch['ingredientitem_set-INITIAL_FORMS'] = '0'
        batch['ingredientitem_set-MIN_NUM_FORMS'] = '0'
        batch['ingredientitem_set-MAX_NUM_FORMS'] = '1000'
        for index, ingredient in enumerate(ingredients):
            ing = Ingredient.objects.get(name=ingredient[0])
            key_head = 'ingredientitem_set-{0}'.format(index)
            batch['{0}-id'.format(key_head)] = ''
            batch['{0}-parent'.format(key_head)] = ''
            batch['{0}-ingredient'.format(key_head)] = ing.pk
            batch['{0}-amount'.format(key_head)] = ingredient[1]
            batch['{0}-temp'.format(key_head)] = ingredient[2]
        key_head = 'ingredientitem_set-{0}'.format('__prefix__')
        batch['{0}-id'.format(key_head)] = ''
        batch['{0}-parent'.format(key_head)] = ''
        batch['{0}-ingredient'.format(key_head)] = ''
        batch['{0}-amount'.format(key_head)] = ''
        batch['{0}-temp'.format(key_head)] = ''
        # samples too
        batch['sample_set-TOTAL_FORMS'] = len(samples)
        batch['sample_set-INITIAL_FORMS'] = '0'
        batch['sample_set-MIN_NUM_FORMS'] = '0'
        batch['sample_set-MAX_NUM_FORMS'] = '1000'
        for index, sample in enumerate(samples):
            ing = Sample.objects.get(name=sample[0])
            key_head = 'sampleitem_set-{0}'.format(index)
            batch['{0}-id'.format(key_head)] = ''
            batch['{0}-parent'.format(key_head)] = ''
            batch['{0}-sample'.format(key_head)] = ing.pk
            batch['{0}-amount'.format(key_head)] = sample[1]
            batch['{0}-temp'.format(key_head)] = sample[2]
        key_head = 'sample_set-{0}'.format('__prefix__')
        batch['{0}-id'.format(key_head)] = ''
        batch['{0}-batch'.format(key_head)] = ''
        batch['{0}-date'.format(key_head)] = ''
        batch['{0}-temp'.format(key_head)] = '60'
        batch['{0}-sg'.format(key_head)] = '0.000'
        batch['{0}-notes'.format(key_head)] = ''
        return batch


class BatchAddTestCase(BatchTestCase):

    def setUp(self):
        super(BatchTestCase, self).setUp()
        self.url = reverse('admin:meadery_batch_add')
        self.batch = BatchTestCase.build_batch(BatchTestCase.fields, BatchTestCase.ingredients, BatchTestCase.samples)

    def batch_exists(before, after):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                self.assertEqual(before, Batch.objects.filter(title=self.batch['title']).exists())
                func(self, *args, **kwds)
                self.assertEqual(after, Batch.objects.filter(title=self.batch['title']).exists())
            return _decorator
        return real_decorator

    def batch_add(ings, respstr):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                batch = BatchTestCase.build_batch(BatchTestCase.fields, [BatchTestCase.ingredients[x] for x in ings], [])
                response = self.client.post(self.url, batch, follow=True)
                self.assertContains(response, respstr)
                func(self, *args, **kwds)
            return _decorator
        return real_decorator

    @batch_exists(False, False)
    @admin_login
    @batch_add([], 'At least one sugar source is required.')
    def test_bad_post_no_data(self):
        pass

    @batch_exists(False, False)
    @admin_login
    @batch_add([0, 1, 2], 'At least one yeast is required.')
    def test_bad_post_no_yeast(self):
        pass

    @batch_exists(False, False)
    @admin_login
    @batch_add([1, 2, 3], 'At least one sugar source is required.')
    def test_bad_post_no_sugar(self):
        pass

    @batch_exists(False, False)
    @admin_login
    @batch_add([0, 1, 3], 'At least two solvents with different temperatures are required.')
    def test_bad_post_not_enough_solvent(self):
        pass

    @batch_exists(False, False)
    @admin_login
    @batch_add([0, 1, 1, 3], 'At least two solvents with different temperatures are required.')
    def test_bad_post_solvents_same_temp(self):
        pass

    @batch_exists(False, True)
    @admin_login
    @batch_add([0, 1, 2, 3], 'The batch &quot;{0} {1}&quot; was added successfully.'.format(BatchTestCase.fields['brewname'], BatchTestCase.fields['batchletter']))
    def test_good_post(self):
        pass


class BatchModifyTestCase(BatchTestCase):
    def setUp(self):
        super(BatchTestCase, self).setUp()
        self.batch = Batch.objects.all()[0]
        self.pk = self.batch.pk
        self.url = reverse('admin:meadery_batch_change', args=(self.pk,))

    @admin_login
    def test_modify(self):
        old_description = self.batch.description
        new_description = old_description + '!!!'
        self.assertNotEqual(old_description, new_description)
        # JMT: this is ... excessive
        batch = BatchTestCase.build_batch(BatchTestCase.fields, BatchTestCase.ingredients, [])
        batch['description'] = new_description
        response = self.client.post(self.url, batch, follow=True)
        self.assertContains(response, 'The batch &quot;{0} {1}&quot; was changed successfully.'.format(BatchTestCase.fields['brewname'], BatchTestCase.fields['batchletter']))
        batch = Batch.objects.get(pk=self.pk)
        self.assertNotEqual(old_description, batch.description)
        self.assertEqual(new_description, batch.description)

    @admin_login
    def test_create_recipe_from_batch(self):
        # JMT: someday test for existing recipes?
        old_recipe_count = Recipe.objects.count()
        button_url = '{0}create_recipe/'.format(self.url)
        response = self.client.get(button_url, follow=True)
        self.assertEqual(response.status_code, 302)
        redirect_target = '{0}{1}'.format('http://testserver',
                                          button_url)
        redirect_chain = [(redirect_target, 302),
                          (redirect_target, 302)]
        self.assertEqual(response.redirect_chain, redirect_chain)
        new_recipe_count = Recipe.objects.count()
        self.assertEqual(new_recipe_count, old_recipe_count + 1)


class BatchCreateProductFromBatchTestCase(BatchModifyTestCase):

    def setUp(self):
        super(BatchModifyTestCase, self).setUp()
        batches = Batch.objects.annotate(num_samples=Count('sample'))
        for prod in Product.objects.all():
            batches = batches.exclude(brewname=prod.brewname, batchletter=prod.batchletter)
        self.batch_with = batches.filter(num_samples__gt=0)[0]
        self.batch_without = batches.filter(num_samples=0)[0]

    def batch_create_product(samples, jars, success):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                func(self, *args, **kwds)
                batch = self.batch_with if samples else self.batch_without
                batch.jars = jars
                batch.save()
                old_product_count = Product.objects.count()
                # JMT: must be a better way
                url = reverse('admin:meadery_batch_change', args=(batch.pk,))
                button_url = '{0}create_product/'.format(url)
                response = self.client.get(button_url, follow=True)
                self.assertEqual(response.status_code, 302)
                redirect_target = '{0}{1}'.format('http://testserver',
                                                  button_url)
                redirect_chain = [(redirect_target, 302),
                                  (redirect_target, 302)]
                self.assertEqual(response.redirect_chain, redirect_chain)
                new_product_count = Product.objects.count()
                if success:
                    self.assertNotEqual(new_product_count, old_product_count)
                else:
                    self.assertEqual(new_product_count, old_product_count)
            return _decorator
        return real_decorator

    def test_modify(self):
        pass

    def test_create_recipe_from_batch(self):
        pass

    @admin_login
    @batch_create_product(True, 0, False)
    def test_samples_no_jars(self):
        pass

    @admin_login
    @batch_create_product(False, 0, False)
    def test_no_samples_no_jars(self):
        pass

    @admin_login
    @batch_create_product(False, 24, False)
    def test_jars_no_samples(self):
        pass

    @admin_login
    @batch_create_product(True, 24, True)
    def test_good_product_does_not_exist(self):
        pass

    @admin_login
    @batch_create_product(True, 24, False)
    def test_good_product_exists(self):
        url = reverse('admin:meadery_batch_change', args=(self.batch_with.pk,))
        button_url = '{0}create_product/'.format(url)
        response = self.client.get(button_url, follow=True)
        self.assertEqual(response.status_code, 302)
        redirect_target = '{0}{1}'.format('http://testserver',
                                          button_url)
        redirect_chain = [(redirect_target, 302),
                          (redirect_target, 302)]
        self.assertEqual(response.redirect_chain, redirect_chain)


class BatchDeleteTestCase(BatchTestCase):

    def setUp(self):
        super(BatchTestCase, self).setUp()
        self.batch = Batch.objects.all()[0]
        self.pk = self.batch.pk
        self.url = reverse('admin:meadery_batch_delete', args=(self.pk,))

    @admin_login
    def test_delete(self):
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, 'Are you sure?')
        # body = self.selenium.find_element_by_tag_name('body')
        # self.assertIn('Are you sure?', body.text)
        # self.assertIn('All of the following related items will be deleted', body.text)
        # self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # self.assertIn('The batch "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        # self.assertFalse(Batch.objects.filter(pk=pk).exists())


class BatchMiscTestCase(BatchTestCase):
    def setUp(self):
        super(BatchTestCase, self).setUp()
        self.url = reverse('admin:meadery_batch_changelist')

    @admin_login
    def test_make_labels(self):
        # Monkey patch generate_labels to use the generic one.
        from . import meadery
        from labels import Label

        def generate_labels(batch):
            return [Label(seq, batch) for seq in xrange(batch.jars)]
        meadery.generate_labels = generate_labels

        fields = {
            'action': 'make_labels',
            'select_across': '0',
            'index': '0',
        }

        # What batches have jars?  (hint: SIP 98 A and SIP 98 C)
        batches = Batch.objects.filter(jars__gt=0).order_by('pk')
        batchnames = ', '.join("{0} {1}".format(batch.brewname, batch.batchletter) for batch in batches)
        # filename = batchnames.lower().replace(', ', '-').replace(' ', '')

        fields['_selected_action'] = tuple([str(batch.pk) for batch in batches])

        response = self.client.post(self.url, fields, follow=True)

        # Two things should occur:
        # - a PDF file containing labels should be downloaded
        #   (check filename?  match file against known good file?)
        # - a message referencing success should appear in the body
        #   (less important)
        # On Travis, the body message is in the response.
        # At home, the PDF is in the response.
        # Why?  Who knows.
        import os
        if os.getenv('TRAVIS', None):
            self.assertContains(response, 'Labels were made for {0}'.format(batchnames))
        else:
            self.assertContains(response, 'ReportLab Generated PDF document')


class SampleTestCase(MeaderyTestCase):
    fixtures = ['meadery']

    fields = {
        'date': '2012-05-31',
        'temp': '60',
        'sg': '1.168',
        'notes': 'Tastes great for a test!'
    }

    def setUp(self):
        super(MeaderyTestCase, self).setUp()
        self.url = reverse('admin:meadery_sample_changelist')

    @staticmethod
    def build_sample(fields):
        sample = SampleTestCase.fields
        sample['batch'] = Batch.objects.all()[0].pk
        return sample


class SampleAddTestCase(SampleTestCase):

    def setUp(self):
        super(SampleTestCase, self).setUp()
        self.url = reverse('admin:meadery_sample_add')

    def sample_exists(before, after):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                self.assertEqual(before, Sample.objects.filter(notes=self.fields['notes']).exists())
                func(self, *args, **kwds)
                self.assertEqual(after, Sample.objects.filter(notes=self.fields['notes']).exists())
            return _decorator
        return real_decorator

    # JMT: consider adding bad tests
    @sample_exists(False, True)
    @admin_login
    def test_good_post(self):
        sample = SampleTestCase.build_sample(SampleTestCase.fields)
        response = self.client.post(self.url, sample, follow=True)
        self.assertContains(response, 'The sample &quot;{0}&quot; was added successfully.'.format(Sample.objects.get(notes=self.fields['notes'])))


class SampleModifyTestCase(SampleTestCase):
    def setUp(self):
        super(SampleTestCase, self).setUp()
        self.sample = Sample.objects.all()[0]
        self.pk = self.sample.pk
        self.url = reverse('admin:meadery_sample_change', args=(self.pk,))

    @admin_login
    def test_modify(self):
        old_notes = self.sample.notes
        new_notes = old_notes + '!!!'
        self.assertNotEqual(old_notes, new_notes)
        # JMT: this is ... excessive
        sample = SampleTestCase.build_sample(SampleTestCase.fields)
        sample['notes'] = new_notes
        response = self.client.post(self.url, sample, follow=True)
        self.assertContains(response, 'The sample &quot;{0}&quot; was changed successfully.'.format(self.sample))
        sample = Sample.objects.get(pk=self.pk)
        self.assertNotEqual(old_notes, sample.notes)
        self.assertEqual(new_notes, sample.notes)


class SampleDeleteTestCase(SampleTestCase):

    def setUp(self):
        super(SampleTestCase, self).setUp()
        self.sample = Sample.objects.all()[0]
        self.pk = self.sample.pk
        self.url = reverse('admin:meadery_sample_delete', args=(self.pk,))

    @admin_login
    def test_delete(self):
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, 'Are you sure?')
        # body = self.selenium.find_element_by_tag_name('body')
        # self.assertIn('Are you sure?', body.text)
        # self.assertIn('All of the following related items will be deleted', body.text)
        # self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # self.assertIn('The sample "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        # self.assertFalse(Sample.objects.filter(pk=pk).exists())


class ProductTestCase(MeaderyTestCase):
    fixtures = ['meadery', 'inventory']

    fields = {
        'title': 'Test Product',
        'description': 'Test description!',
        'category': '241',
        'brewname': 'SIP 99',
        'batchletter': 'A',
        # 'is_active': 'on'
        'meta_keywords': 'bogus',
        'meta_description': 'bogus',
        'brewed_date': '2013-05-01',
        'brewed_sg': '1.126',
        'bottled_date': '2013-05-31',
        'bottled_sg': '0.996',
        'abv': '17.33'
    }

    def setUp(self):
        super(MeaderyTestCase, self).setUp()
        self.url = reverse('admin:meadery_product_changelist')

    @staticmethod
    def build_product(fields):
        product = {}
        for key, value in ProductTestCase.fields.items():
            product[key] = value
        return product


class ProductAddTestCase(ProductTestCase):
    def setUp(self):
        super(ProductTestCase, self).setUp()
        self.url = reverse('admin:meadery_product_add')
        self.product = ProductTestCase.build_product(ProductTestCase.fields)

    def product_exists(before, after):
        def real_decorator(func):
            def _decorator(self, *args, **kwds):
                self.assertEqual(before, Product.objects.filter(title=self.product['title']).exists())
                func(self, *args, **kwds)
                self.assertEqual(after, Product.objects.filter(title=self.product['title']).exists())
            return _decorator
        return real_decorator

    # JMT: write tests that check for bad posts
    @product_exists(False, True)
    @admin_login
    def test_good_post(self):
        product = ProductTestCase.build_product(ProductTestCase.fields)
        response = self.client.post(self.url, product, follow=True)
        self.assertContains(response, 'The product &quot;{0} {1}&quot; was added successfully.'.format(ProductTestCase.fields['brewname'], ProductTestCase.fields['batchletter']))


class ProductModifyTestCase(ProductTestCase):
    def setUp(self):
        super(ProductTestCase, self).setUp()
        self.product = Product.objects.all()[0]
        self.pk = self.product.pk
        self.url = reverse('admin:meadery_product_change', args=(self.pk,))

    @admin_login
    def test_modify(self):
        old_description = self.product.description
        new_description = old_description + '!!!'
        self.assertNotEqual(old_description, new_description)
        # JMT: this is ... excessive
        product = ProductTestCase.build_product(ProductTestCase.fields)
        product['description'] = new_description
        response = self.client.post(self.url, product, follow=True)
        self.assertContains(response, 'The product &quot;{0} {1}&quot; was changed successfully.'.format(ProductTestCase.fields['brewname'], ProductTestCase.fields['batchletter']))
        product = Product.objects.get(pk=self.pk)
        self.assertNotEqual(old_description, product.description)
        self.assertEqual(new_description, product.description)


class ProductDeleteTestCase(ProductTestCase):

    def setUp(self):
        super(ProductTestCase, self).setUp()
        self.product = Product.objects.all()[0]
        self.pk = self.product.pk
        self.url = reverse('admin:meadery_product_delete', args=(self.pk,))

    @admin_login
    def test_delete(self):
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, 'Are you sure?')
        # body = self.selenium.find_element_by_tag_name('body')
        # self.assertIn('Are you sure?', body.text)
        # self.assertIn('All of the following related items will be deleted', body.text)
        # self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # self.assertIn('The product "%s" was deleted successfully.' % name, self.selenium.find_element_by_tag_name('body').text)
        # self.assertFalse(Product.objects.filter(pk=pk).exists())
        # JMT: should also check jar count to ensure jars are deleted too!
