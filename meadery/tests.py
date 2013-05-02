from decimal import Decimal
from django.test import TestCase
from models import Honey, Water, Flavor, Yeast, HoneyItem, CoolItem, WarmItem, FlavorItem, YeastItem, Recipe, Batch, Sample
from catalog.models import Category


class RecipeTest(TestCase):
    def setUp(self):
        """ Using standard recipe for testing:

        4.540kg honey (10 lbs)
        9.467L warm water (2.5 gal) at 140 deg F
        9.467L cool water (2.5 gal) at 70 deg F
        no flavor
        no yeast
        """

        self.honey = Honey()
        self.honey.save()

        self.water = Water()
        self.water.save()

        self.yeast = Yeast()
        self.yeast.tolerance = 18
        self.yeast.save()

        self.recipe = Recipe()
        self.recipe.save()

        self.honey_item = HoneyItem()
        self.honey_item.honey = self.honey
        self.honey_item.mass = Decimal('4.540')
        self.honey_item.temp = 70
        self.honey_item.recipe = self.recipe
        self.honey_item.save()

        self.warm_item = WarmItem()
        self.warm_item.water = self.water
        self.warm_item.volume = Decimal('9.467')
        self.warm_item.temp = 140
        self.warm_item.recipe = self.recipe
        self.warm_item.save()

        self.cool_item = CoolItem()
        self.cool_item.water = self.water
        self.cool_item.volume = Decimal('9.467')
        self.cool_item.temp = 70
        self.cool_item.recipe = self.recipe
        self.cool_item.save()

    def test_brew_mass(self):
        """
        Test brewing volume prediction.

        Standard recipe should produce 23.474 kilograms.
        """
        self.assertEqual(self.recipe.brew_mass, Decimal('23.474'))

    def test_brew_volume(self):
        """
        Test brewing volume prediction.

        Standard recipe should produce 22.127 liters.
        """
        self.assertEqual(self.recipe.brew_volume, Decimal('22.127'))

    def test_brew_sg(self):
        """
        Test brewing specific gravity prediction.

        Standard recipe should have a specific gravity of 1.061.
        """
        self.assertEqual(self.recipe.brew_sg, Decimal('1.061'))

    def test_brew_temp(self):
        """
        Test brewing temperature prediction.

        Standard recipe should have a brew temperature of 100 deg F.

        """
        self.assertEqual(self.recipe.brew_temp, 100)

    def test_category(self):
        """
        Test brewing categories.

        Standard recipe should be Recipe.DRY.

        """
        self.assertEqual(self.recipe.suggested_category(), Recipe.DRY)

        # Now tweak the recipes
        dump_recipe = Recipe()
        dump_recipe.save()

        new_honey = Honey()
        new_honey.type = Honey.MALT
        new_honey.save()
        new_honey_item = HoneyItem()
        new_honey_item.honey = new_honey
        new_honey_item.mass = Decimal('4.540')
        new_honey_item.temp = 70
        new_honey_item.recipe = self.recipe
        new_honey_item.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.BRAGGOT)
        new_honey.type = Honey.OTHER
        new_honey.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.OPEN_CATEGORY)
        new_honey_item.recipe = dump_recipe
        new_honey_item.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.DRY)

        new_water = Water()
        new_water.type = Water.APPLE_JUICE
        new_water.save()
        new_cool_item = CoolItem()
        new_cool_item.water = new_water
        new_cool_item.volume = Decimal('9.467')
        new_cool_item.temp = 70
        new_cool_item.recipe = self.recipe
        new_cool_item.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.CYSER)
        new_water.type = Water.OTHER
        new_water.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.OPEN_CATEGORY)
        new_cool_item.recipe = dump_recipe
        new_cool_item.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.DRY)

        new_flavor = Flavor()
        new_flavor.type = Flavor.FRUIT
        new_flavor.save()
        new_flavor_item = FlavorItem()
        new_flavor_item.flavor = new_flavor
        new_flavor_item.amount = 70
        new_flavor_item.recipe = self.recipe
        new_flavor_item.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.OTHER_FRUIT_MELOMEL)
        new_flavor.type = Flavor.OTHER
        new_flavor.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.OPEN_CATEGORY)
        new_flavor_item.recipe = dump_recipe
        new_flavor_item.save()
        self.assertEqual(self.recipe.suggested_category(), Recipe.DRY)
