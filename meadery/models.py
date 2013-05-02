from __future__ import division
from django.db import models
from catalog.models import Category
from decimal import Decimal


# Stuff to consider for this app:
# - consider writing mixins for temperature (conversion, specifically) and specific gravity and specific heat
# - consider writing something for metric/US/Imperial/whatever
# - consider making dropdown lists or something similarly sophisticated for appellations
# - consider writing decorator for honey_mass == 0 checks


class Ingredient(models.Model):
    """ Ingredients are found in recipes. """
    name = models.CharField('Ingredient Name', max_length=40, help_text='Ingredient name')
    is_natural = models.BooleanField(default=False, help_text='TRUE if the ingredient does not contain added color, artificial flavors, or synthetic substances.')
    # JMT: may need to change appellation to a dropdown list
    appellation = models.CharField('Appellation', max_length=20, help_text='Where the ingredient was made (i.e., Oregon, California, Brazil)')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        abstract = True


class Honey(Ingredient):
    """
    Honey is the source of fermentable sugars.

    Other potential sugar sources include agave nectar.

    The units for honey are kilograms.
    """
    sg = models.DecimalField('Specific Gravity', max_digits=4, decimal_places=3, default=Decimal('1.422'), help_text='Specific gravity of honey (default value should be fine)')
    sh = models.DecimalField('Specific Heat', max_digits=3, decimal_places=2, default=Decimal('0.57'), help_text='Specific heat of honey (default value should be fine)')
    # Individual types of sugar sources.
    HONEY = 1
    MALT = 2
    OTHER = 3
    HONEY_TYPES = ((HONEY, 'Honey'),
                   (MALT, 'Malt'),
                   (OTHER, 'Other'))
    type = models.IntegerField(choices=HONEY_TYPES, default=HONEY)


class Water(Ingredient):
    """
    Water is the solvent in which the honey is dissolved and fermented.

    Other potential solvents include apple juice.

    The units for water are liters.
    """
    sg = models.DecimalField('Specific Gravity', max_digits=4, decimal_places=3, default=Decimal('1.000'), help_text='Specific gravity of water (default value should be fine)')
    sh = models.DecimalField('Specific Heat', max_digits=3, decimal_places=2, default=Decimal('1.00'), help_text='Specific heat of water (default value should be fine)')
    # Individual types of solvents.
    WATER = 1
    APPLE_JUICE = 2
    GRAPE_JUICE = 3
    FRUIT_JUICE = 4
    OTHER = 5
    WATER_TYPES = ((WATER, 'Water'),
                   (APPLE_JUICE, 'Apple Juice'),
                   (GRAPE_JUICE, 'Grape Juice'),
                   (FRUIT_JUICE, 'Fruit Juice'),
                   (OTHER, 'Other'))
    type = models.IntegerField(choices=WATER_TYPES, default=WATER)


class Flavor(Ingredient):
    """
    Flavors are ingredients which are not considered honey or water, which
    means that their effect on increasing fermentable sugars or volume
    of output is not considered.

    These ingredients are often bagged and removed during racking.

    The units for flavors are specific to each flavor.

    """
    units = models.CharField('Units', max_length=12, help_text='Units used to measure ingredient')
    # Individual types of flavors.
    SPICE = 1
    APPLE = 2
    GRAPE = 3
    FRUIT = 4
    OTHER = 5
    FLAVOR_TYPES = ((SPICE, 'Spice'),
                    (APPLE, 'Apple'),
                    (GRAPE, 'Grape'),
                    (FRUIT, 'Fruit'),
                    (OTHER, 'Other'))
    type = models.IntegerField(choices=FLAVOR_TYPES, default=SPICE)


class Yeast(Ingredient):
    """ Yeasts are what converts sugars into alcohol. """
    tolerance = models.IntegerField('Alcohol tolerance', help_text='Maximum alcohol tolerance (in percent)')
    # Individual types of yeast.
    DRY = 1
    WET = 2
    YEAST_TYPES = ((DRY, 'Dry'),
                   (WET, 'Wet'))
    type = models.IntegerField(choices=YEAST_TYPES, default=DRY)

    # JMT: DRY violation
    @property
    def maxdeltasg(self):
        """ Maximum change in specific gravity based on alcohol tolerance. """
        return Decimal(self.tolerance / 100.0 * 0.75).quantize(Decimal('0.001'))


class HoneyItem(models.Model):
    honey = models.ForeignKey(Honey)
    mass = models.DecimalField(max_digits=5, decimal_places=3, help_text='Mass of honey in kilograms (1 lb = 0.454 kg)')
    recipe = models.ForeignKey('Recipe')

    @property
    def volume(self):
        return Decimal(self.mass / self.honey.sg).quantize(Decimal('0.001'))


class WaterItem(models.Model):
    water = models.ForeignKey(Water)
    volume = models.DecimalField(max_digits=5, decimal_places=3, help_text='Volume of water in liters (1 gal = 3.785 L)')
    recipe = models.ForeignKey('Recipe')

    @property
    def mass(self):
        return Decimal(self.volume * self.water.sg).quantize(Decimal('0.001'))


class CoolItem(WaterItem):
    pass


class WarmItem(WaterItem):
    pass


class FlavorItem(models.Model):
    flavor = models.ForeignKey(Flavor)
    amount = models.FloatField(help_text='Amount of flavor ingredient')
    recipe = models.ForeignKey('Recipe')


class YeastItem(models.Model):
    yeast = models.ForeignKey(Yeast)
    amount = models.IntegerField(help_text='Number of units of yeast')
    recipe = models.ForeignKey('Recipe')


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

    title = models.CharField(max_length=40, help_text='Recipe title')
    description = models.TextField(help_text='Description of product.')
    category = models.ForeignKey(Category)
    warm_temp = models.IntegerField(help_text='Temperature of warm water in degrees Fahrenheit')
    cool_temp = models.IntegerField(help_text='Temperature of cool water in degrees Fahrenheit')

    @property
    def name(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title

    @property
    def honey_items(self):
        return HoneyItem.objects.filter(recipe=self)

    @property
    def honey_mass(self):
        return sum([item.mass for item in self.honey_items])

    @property
    def honey_volume(self):
        return sum([item.volume for item in self.honey_items])

    @property
    def honey_sg(self):
        honey_mass = self.honey_mass
        if honey_mass > 0:
            return sum([item.honey.sg*(item.mass/honey_mass) for item in self.honey_items])
        else:
            return None

    @property
    def honey_sh(self):
        honey_mass = self.honey_mass
        if honey_mass > 0:
            return sum([item.honey.sh*(item.mass/honey_mass) for item in self.honey_items])
        else:
            return None

    @property
    def cool_items(self):
        return CoolItem.objects.filter(recipe=self)

    @property
    def cool_mass(self):
        return sum([item.mass for item in self.cool_items])

    @property
    def cool_volume(self):
        return sum([item.volume for item in self.cool_items])

    @property
    def cool_sg(self):
        cool_mass = self.cool_mass
        if cool_mass > 0:
            return sum([item.water.sg*(item.mass/cool_mass) for item in self.cool_items])
        else:
            return None

    @property
    def cool_sh(self):
        cool_mass = self.cool_mass
        if cool_mass > 0:
            return sum([item.water.sh*(item.mass/cool_mass) for item in self.cool_items])
        else:
            return None

    @property
    def warm_items(self):
        return WarmItem.objects.filter(recipe=self)

    @property
    def warm_mass(self):
        return sum([item.mass for item in self.warm_items])

    @property
    def warm_volume(self):
        return sum([item.volume for item in self.warm_items])

    @property
    def warm_sg(self):
        warm_mass = self.warm_mass
        if warm_mass > 0:
            return sum([item.water.sg*(item.mass/warm_mass) for item in self.warm_items])
        else:
            return None

    @property
    def warm_sh(self):
        warm_mass = self.warm_mass
        if warm_mass > 0:
            return sum([item.water.sh*(item.mass/warm_mass) for item in self.warm_items])
        else:
            return None

    # JMT: for now, flavors and yeast are treated as having zero impact on mass or volume.

    @property
    def flavor_items(self):
        return FlavorItem.objects.filter(recipe=self)

    @property
    def yeast_items(self):
        return YeastItem.objects.filter(recipe=self)

    @property
    def brew_mass(self):
        return self.honey_mass + self.cool_mass + self.warm_mass

    @property
    def brew_volume(self):
        return self.honey_volume + self.cool_volume + self.warm_volume

    @property
    def brew_sg(self):
        # SG of total is total mass divided by total volume.
        if self.brew_volume > 0:
            return Decimal(self.brew_mass/self.brew_volume).quantize(Decimal('0.001'))
        else:
            return Decimal('0.000')

    @property
    def brew_temp(self):
        # Temperatures are converted from Fahrenheit to Celsius and back.
        warm_tempC = Decimal((self.warm_temp-32)/1.8)
        cool_tempC = Decimal((self.cool_temp-32)/1.8)
        warm_heat = warm_tempC * self.warm_mass * self.warm_sh
        cool_heat = cool_tempC * self.cool_mass * self.cool_sh
        # Honey is assumed to be at same temperature as cool water.
        honey_heat = cool_tempC * self.honey_mass * self.honey_sh
        # Totals
        total_heat = warm_heat + cool_heat + honey_heat
        total_heat_capacity = warm_heat/warm_tempC + cool_heat/cool_tempC + honey_heat/cool_tempC
        if total_heat_capacity > 0:
            # Final temperature in Celsius.
            brew_tempC = total_heat/total_heat_capacity
            return int((float(brew_tempC)*1.8)+32)
        else:
            return None

    def all_natural(self):
        # TRUE if all ingredients are natural
        # JMT: skipping yeast at the moment
        honey_is_natural = all([item.honey.is_natural for item in self.honey_items])
        cool_is_natural = all([item.water.is_natural for item in self.cool_items])
        warm_is_natural = all([item.water.is_natural for item in self.warm_items])
        flavor_is_natural = all([item.flavor.is_natural for item in self.flavor_items])
        return honey_is_natural and cool_is_natural and warm_is_natural and flavor_is_natural

    def appellation(self):
        # Proper implementation of appellation testing is very complex.  See 27 CFR 4.25(b) for more information.
        honey_appellations = list(set([item.honey.appellation for item in self.honey_items]))
        cool_appellations = list(set([item.water.appellation for item in self.cool_items]))
        warm_appellations = list(set([item.water.appellation for item in self.warm_items]))
        flavor_appellations = list(set([item.flavor.appellation for item in self.flavor_items]))
        
        total_appellations = list(set(honey_appellations+cool_appellations+warm_appellations+flavor_appellations))
        if len(total_appellations) == 1:
            return total_appellations[0]
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
    jars = models.IntegerField(help_text='Number of jars actually produced from this batch.')

    @property
    def name(self):
        return '%s %s' % (self.brewname, self.batchletter)

    def __unicode__(self):
        return u'%s %s' % (self.brewname, self.batchletter)

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
        # Convert temperature from Fahrenheit to Celsius first.
        tempC = int((self.temp-32)/1.8)
        return self.sg + Decimal(Sample.deltasg[tempC])

