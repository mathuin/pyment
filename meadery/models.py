from django.db import models
from catalog.models import Category
from decimal import Decimal


class Ingredient(models.Model):
    """ Ingredients are found in recipes. """
    name = models.CharField(max_length=40, help_text='Ingredient name')
    natural = models.BooleanField(default=False, help_text='TRUE if the ingredient does not contain added color, artificial flavors, or synthetic substances.')
    # JMT: may need to change appellation to a dropdown list
    appellation = models.CharField(max_length=20, help_text='Where the ingredient was made (i.e., Oregon, California, Brazil)')


class Honey(Ingredient):
    """
    Honey is the source of fermentable sugars.

    Other potential sugar sources include agave nectar.

    The units for honey are kilograms.
    """
    # JMT: should do something about pounds/kilograms
    # JMT: may need to make specific gravity its own class
    sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('1.422'), help_text='Specific gravity of honey (default value should be fine)')
    sh = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.57'), help_text='Specific heat of honey (default value should be fine)')

    # converting mass to volume
    def volume(self, mass):
        return Decimal(mass / self.sg).quantize(Decimal('0.001'))


class Water(Ingredient):
    """
    Water is the solvent in which the honey is dissolved and fermented.

    Other potential solvents include apple juice.

    The units for water are liters.
    """
    # JMT: should do something about gallons/liters
    # JMT: may need to make specific gravity its own class
    sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('1.000'), help_text='Specific gravity of water (default value should be fine)')
    sh = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('1.00'), help_text='Specific heat of water (default value should be fine)')

    # converting volume to mass
    def mass(self, volume):
        return Decimal(volume * self.sg).quantize(Decimal('0.001'))


class Flavor(Ingredient):
    """
    Flavors are ingredients which are not considered honey or water, which
    means that their effect on increasing fermentable sugars or volume
    of output is not considered.

    These ingredients are often bagged and removed during racking.

    The units for flavors are specific to each flavor.

    """
    units = models.CharField(max_length=12, help_text='Units used to measure ingredient')


class Yeast(Ingredient):
    """ Yeasts are what converts sugars into alcohol. """
    # JMT: what info do I need to store here?  alcohol tolerance?
    pass


class Recipe(models.Model):
    """
    Recipes are composed of ingredients and directions.

    Ingredients in recipes include amount of ingredient as well as type.

    The directions portion of the recipe is static:

    1.  Add honey to bucket.
    2.  Add hot water to bucket and stir.
    3.  Add cool water to bucket and stir.
    4.  Add flavor to bucket.
    5.  Pitch yeast.

    Recipes are copied to batches, which include actual amounts.
    """

    # A proper implementation would support multiple ingredients:
    # [(ingredient, amount), ...]
    # then do the math together at the end!
    title = models.CharField(max_length=40, help_text='Recipe title')
    description = models.TextField(help_text='Description of product.')
    category = models.ForeignKey(Category)
    # honey information
    honey = models.ForeignKey(Honey)
    honey_mass = models.DecimalField(max_digits=5, decimal_places=3, help_text='Mass of honey in kilograms (1 lb = 0.454 g)')
    # water information
    warm_water = models.ForeignKey(Water, related_name='warm_waters')
    warm_volume = models.DecimalField(max_digits=5, decimal_places=3, help_text='Volume of warm water in liters (1 gal = 3.785 L)')
    warm_temp = models.IntegerField(help_text='Temperature of warm water in degrees Fahrenheit')
    cool_water = models.ForeignKey(Water, related_name='cool_waters')
    cool_volume = models.DecimalField(max_digits=5, decimal_places=3, help_text='Volume of cool water in liters (1 gal = 3.785 L)')
    cool_temp = models.IntegerField(help_text='Temperature of cool water in degrees Fahrenheit')
    # JMT: flavors are optional and have variable amounts -- need some way to handle no-flavor
    # probably a special flavor of 'None'
    flavor = models.ForeignKey(Flavor)
    flavor_amount = models.FloatField(help_text='Amount of flavor ingredient.')
    yeast = models.ForeignKey(Yeast)

    def brew_temp(self):
        # Temperatures are converted from Fahrenheit to Celsius and back.
        warm_tempC = Decimal((self.warm_temp-32)/1.8)
        cool_tempC = Decimal((self.cool_temp-32)/1.8)
        warm_heat = warm_tempC * self.warm_water.mass(self.warm_volume) * self.warm_water.sh
        cool_heat = cool_tempC * self.cool_water.mass(self.cool_volume) * self.cool_water.sh
        # Honey is assumed to be at same temperature as cool water.
        honey_heat = cool_tempC * self.honey_mass * self.honey.sh
        # Totals
        total_heat = warm_heat + cool_heat + honey_heat
        total_heat_capacity = warm_heat/warm_tempC + cool_heat/cool_tempC + honey_heat/cool_tempC
        # Final temperature in Celsius.
        brew_tempC = total_heat/total_heat_capacity
        return int((float(brew_tempC)*1.8)+32)

    def brew_sg(self):
        # SG of total is total mass divided by total volume.
        total_mass = self.warm_water.mass(self.warm_volume) + self.cool_water.mass(self.cool_volume) + self.honey_mass
        total_volume = self.warm_volume + self.cool_volume + self.honey.volume(self.honey_mass)
        return Decimal(total_mass/total_volume).quantize(Decimal('0.001'))

    def all_natural(self):
        # TRUE if all ingredients are natural
        # JMT: skipping yeast at the moment
        # JMT: need to handle the no-flavor case
        return self.honey.natural and self.warm_water.natural and self.cool_water.natural and self.flavor.natural

    def appellation(self):
        # Proper implementation of appellation testing is very complex.  See 27 CFR 4.25(b) for more information.
        # For now, try this:
        #   if all ingredients have the same appellation, use that appellation
        #   else None
        # JMT: need to handle the no-flavor case
        if self.honey.appellation == self.warm_water.appellation and self.honey.appellation == self.cool_water.appellation and self.honey.appellation == self.flavor.appellation:
            return self.honey.appellation
        else:
            return None


class Batch(Recipe):
    """
    Batches are actual implementations of recipes.

    Products can be created from batches.
    """

    recipe = models.ForeignKey(Recipe, related_name='originals')
    brewname = models.CharField('Brew Name', max_length=8, help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')
    jars = models.IntegerField(help_text='Number of jars produced from this batch.')

    @property
    def abv(self):
        zero = Decimal('0.000')
        if self.sample_set.count() > 1:
            firstsg = self.sample_set.order_by('date')[0].corrsg
            lastsg = self.sample_set.order_by('-date')[0].corrsg
            if firstsg != zero and lastsg != zero and firstsg > lastsg:
                return Decimal('100')*(firstsg - lastsg)/Decimal('0.75')
            else:
                return None
        else:
            return None

    # methods:
    # creating a new batch:
    #   copy all values from the source recipe into the real one
    # save batch as recipe:
    #   does what it says!
    # admin site edit:
    #   when certain values change, change the dependent read-only
    #   values after saving!
    #   also do this when adding samples if at all possible.
    # generate a product:
    #   copy all relevant values to the product, with dummy images
    #   (or remove the stupid image requirement thing!)
    #   set product to inactive
    # print labels:
    #   using final SG and description values, checking appellation


class Sample(models.Model):
    """ Samples are small collections of data. """
    batch = models.ForeignKey(Batch)
    date = models.DateTimeField(auto_now_add=True)
    temp = models.IntegerField(default=60, help_text='Temperature of mead in degrees Fahrenheit')
    sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'), help_text='Specific gravity of mead')
    notes = models.TextField(help_text='Tasting notes')

    deltasg = [-0.0007, -0.0008, -0.0008, -0.0009, -0.0009,
               -0.0009, -0.0008, -0.0008, -0.0007, -0.0007,
               -0.0006, -0.0005, -0.0004, -0.0003, -0.0001,
               0.0000,  0.0002,  0.0003,  0.0005,  0.0007,
               0.0009,  0.0011,  0.0013,  0.0016,  0.0018,
               0.0021,  0.0023,  0.0026,  0.0029,  0.0032,
               0.0035,  0.0038,  0.0041,  0.0044,  0.0047,
               0.0051,  0.0054,  0.0058,  0.0061,  0.0065,
               0.0069,  0.0073,  0.0077,  0.0081,  0.0085,
               0.0089,  0.0093,  0.0097,  0.0102,  0.0106]

    @property
    def corrsg(self):
        # JMT: convert from Fahrenheit to Celsius to correct SG
        tempC = int((self.temp-32)/1.8)
        return self.sg + Decimal(Sample.deltasg[tempC])
