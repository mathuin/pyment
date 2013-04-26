from django.db import models
from catalog.models import Category


class Ingredient(models.Model):
    """ Ingredients are found in recipes. """
    name = models.CharField(max_length=40, help_text='Unique name for ingredient')
    natural = models.BooleanField(default=False, help_text='TRUE if the ingredient does not contain added color, artificial flavors, or synthetic substances.')
    # JMT: may need to change appellation to a dropdown list
    appellation = models.CharField(max_length=20, help_text='Where the ingredient was made (i.e., Oregon, California, Brazil)')


class Honey(Ingredient):
    """
    Honey is the source of fermentable sugars.

    Other potential sugar sources include agave nectar.

    The units for honey are grams.
    """
    # JMT: should do something about pounds/grams
    # JMT: may need to make specific gravity its own class
    sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('1.422'), help_text='Specific gravity of raw material (default value should be fine)')
    sh = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.57'), help_text='Specific heat of honey (default value should be fine)')


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


class Flavor(Ingredient):
    """
    Flavors are ingredients which are not considered honey or water.

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

    # Recipes are composed of ingredients and are imported into batches.
    title = models.CharField(max_length=40, help_text='Recipe title')
    description = models.TextField(help_text='Description of product.')
    category = models.ForeignKey(Category)
    # honey information
    # JMT: only one ingredient of each type is currently supported
    # A proper implementation would support multiple ingredients:
    # [(ingredient, amount), ...]
    # then do the math together at the end!
    honey = models.ForeignKey(Honey)
    honey_amount = models.IntegerField(help_text='Amount of honey in grams (1 lb = 454 g)')
    # water information
    # JMT: same water is used for warm and cool water for now
    water = models.ForeignKey(Water)
    warm_amount = models.FloatField(help_text='Amount of warm water in liters (1 gal = 3.785 L)')
    warm_temp = models.IntegerField(help_text='Temperature of warm water in degrees Fahrenheit')
    cool_amount = models.FloatField(help_text='Amount of cool water in liters (1 gal = 3.785 L)')
    cool_temp = models.IntegerField(help_text='Temperature of cool water in degrees Fahrenheit')
    flavor = models.ForeignKey(Flavor)
    flavor_amount = models.FloatField(help_text='Amount of flavor ingredient.')
    yeast = models.ForeignKey(Yeast)
    # methods:
    # predict brew temp:
    #   sum mass times specific heat
    #   divide by total mass = specific heat of mix
    #   sum mass times specific heat times delta temp
    #   - 0 for honey and cool, warm-cool for warm
    #   divide by specific heat of mix = delta for mix
    #   add cool to get final answer
    # predict brew specific gravity:
    #   calculate brew temp
    #   sum mass times specific gravity
    #   divide by total mass = specific gravity of mix
    #   apply temp correction
    # is recipe 'all natural'?
    #   if all ingredients are natural, it is
    # does recipe qualify for appellation?
    #   CRAZY COMPLICATED 27 CFR 4.25(b) -- for now, do it simple
    #   if all ingredients have the same appellation, use that appellation
    #   else None


class Batch(Recipe):
    """
    Batches are actual implementations of recipes.

    Products can be created from batches.
    """

    recipe = models.ForeignKey(Recipe)
    brewname = models.CharField('Brew Name', max_length=8, help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')

    @property
    def abv(self):
        zero = Decimal('0.000')
        if self.sample_set.count() > 1:
            # JMT: this may not be optimal
            first = self.sample_set.order_by('date')[0]
            last = self.sample_set.order_by('-date')[0]
            # JMT: not using corrected SG, should fix
            if first.sg != zero and last.sg != zero and first.sg > last.sg:
                return '%0.2f' % (Decimal('100')*(first.sg - last.sg)/Decimal('0.75'))
            else:
                return '---'
        else:
            return '---'

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
    temp = models.IntegerField(help_text='Temperature of warm water in degrees Fahrenheit')
    sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'), help_text='Specific gravity of mead')
    notes = models.TextField(help_text='Tasting notes')
    # methods:
    # corrsg = correct specific gravity
