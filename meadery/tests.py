from decimal import Decimal
from django.test import TestCase
from meadery.models import Honey, Water, Flavor, Yeast, Recipe


class HoneyTest(TestCase):
    def setUp(self):
        self.honey = Honey()
        self.honey_mass = Decimal('4.540')

    def test_volume(self):
        """
        Test conversion from mass to volume.
        """
        self.assertEqual(self.honey.volume(self.honey_mass), Decimal('3.193'))


class WaterTest(TestCase):
    def setUp(self):
        self.water = Water()
        self.water_volume = Decimal('9.467')

    def test_mass(self):
        """
        Test conversion from volume to mass.
        """
        self.assertEqual(self.water.mass(self.water_volume), Decimal('9.467'))


class RecipeTest(TestCase):
    def setUp(self):
        """ Using standard recipe for testing:

        4.540kg honey (10 lbs)
        9.467L warm water (2.5 gal) at 140 deg F
        9.467L cool water (2.5 gal) at 70 deg F
        no flavor
        no yeast
        """

        self.recipe = Recipe()
        self.recipe.honey = Honey()
        self.recipe.honey_mass = Decimal('4.540')
        self.recipe.warm_water = Water()
        self.recipe.warm_volume = Decimal('9.467')
        self.recipe.warm_temp = 140
        self.recipe.cool_water = Water()
        self.recipe.cool_volume = Decimal('9.467')
        self.recipe.cool_temp = 70
        self.recipe.flavor = Flavor()
        self.recipe.yeast = Yeast()

    def test_brew_temp(self):
        """
        Test brewing temperature prediction.

        Standard recipe should have a brew temperature of 100 deg F.

        """
        self.assertEqual(self.recipe.brew_temp(), 100)

    def test_brew_sg(self):
        """
        Test brewing specific gravity prediction.

        Standard recipe should have a specific gravity of 1.061.
        """
        self.assertEqual(self.recipe.brew_sg(), Decimal('1.061'))

    def test_volume(self):
        """
        Test brewing volume prediction.

        Standard recipe should produce 22.127 liters.
        """
        self.assertEqual(self.recipe.brew_volume(), Decimal('22.127'))
