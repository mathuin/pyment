from __future__ import division
from django.db import models
from django.template.defaultfilters import slugify
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


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

    Other potential sugar sources include malted barley and maple syrup.

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

    Other potential solvents include apple juice, grape juice, and other fruit juice.

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
        return Decimal(self.tolerance / Decimal('100.0') * Decimal('0.75')).quantize(Decimal('0.001'))


class IngredientItem(models.Model):
    recipe = models.ForeignKey('Recipe')

    class Meta:
        abstract = True


class HoneyItem(IngredientItem):
    honey = models.ForeignKey(Honey)
    mass = models.DecimalField(max_digits=5, decimal_places=3, help_text='Mass of honey in kilograms (1 lb = 0.454 kg)')
    temp = models.IntegerField(help_text='Temperature of honey in degrees Fahrenheit')

    @property
    def volume(self):
        return Decimal(self.mass / self.honey.sg).quantize(Decimal('0.001'))

    # JMT: DRY violation
    @property
    def to_c(self):
        return Decimal((self.temp-32)/1.8)


class WaterItem(IngredientItem):
    water = models.ForeignKey(Water)
    volume = models.DecimalField(max_digits=5, decimal_places=3, help_text='Volume of water in liters (1 gal = 3.785 L)')
    temp = models.IntegerField(help_text='Temperature of water in degrees Fahrenheit')

    class Meta:
        abstract = True

    @property
    def mass(self):
        return Decimal(self.volume * self.water.sg).quantize(Decimal('0.001'))

    # JMT: DRY violation
    @property
    def to_c(self):
        return Decimal((self.temp-32)/1.8)


class CoolItem(WaterItem):
    pass


class WarmItem(WaterItem):
    pass


class FlavorItem(IngredientItem):
    flavor = models.ForeignKey(Flavor)
    amount = models.FloatField(help_text='Amount of flavor ingredient')


class YeastItem(IngredientItem):
    yeast = models.ForeignKey(Yeast)
    amount = models.IntegerField(help_text='Number of units of yeast')


MEAD_CATEGORIES = {'dry': 241,
                   'semi_sweet': 242,
                   'sweet': 243,
                   'cyser': 251,
                   'pyment': 252,
                   'other_fruit_melomel': 253,
                   'metheglin': 261,
                   'braggot': 262,
                   'open_category': 263}
MEAD_CHOICES = ((MEAD_CATEGORIES['dry'], 'Dry Mead'),
                (MEAD_CATEGORIES['semi_sweet'], 'Semi-Sweet Mead'),
                (MEAD_CATEGORIES['sweet'], 'Sweet Mead'),
                (MEAD_CATEGORIES['cyser'], 'Cyser'),
                (MEAD_CATEGORIES['pyment'], 'Pyment'),
                (MEAD_CATEGORIES['other_fruit_melomel'], 'Other Fruit Melomel'),
                (MEAD_CATEGORIES['metheglin'], 'Metheglin'),
                (MEAD_CATEGORIES['braggot'], 'Braggot'),
                (MEAD_CATEGORIES['open_category'], 'Open Category Mead'))
MEAD_DESCRIPTIONS = {MEAD_CATEGORIES['dry']: 'A traditional mead with subtle honey aroma but no significant aromatics. Minimal residual sweetness with a dry finish, and a light to medium body. Similar to a dry white wine. (Based on BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['semi_sweet']: 'A traditional mead with noticeable honey aroma and subtle to moderate residual sweetness with a medium-dry finish.  Body is medium-light to medium-full.  Similar to a semi-sweet (or medium-dry) white wine.  (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['sweet']: 'A traditional mead with dominating honey aroma, often moderately to strongly sweet.  The body is generally medium-full to full, and may seem like a dessert wine.  (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['cyser']: 'A mead made from honey and apple juice, with a variety of flavors.  (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['pyment']: 'A melomel made from grapes or grape juice.  (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['other_fruit_melomel']: 'A mead made from honey and fruit (not grapes or apples).  (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['metheglin']: 'A spiced mead.  (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['braggot']: 'A mead made with malt. (thanks to BJCP Style Guidelines 2008)',
                     MEAD_CATEGORIES['open_category']: 'A honey-based beverage that either combines ingredients from two or more of the other mead sub-categories, is a historical or indigenous mead (e.g., tej, Polish meads), or is a mead that does not fit into any other category.  Any specialty or experimental mead using additional sources of fermentables (e.g., maple syrup, molasses, brown sugar, or agave nectar), additional ingredients (e.g., vegetables, liquors, smoke, etc.), alternative processes (e.g., icing, oak-aging) or other unusual ingredient, process, or technique would also be appropriate in this category.'}


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
    category = models.IntegerField(choices=MEAD_CHOICES, default=MEAD_CATEGORIES['dry'])

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
    def honey_tempC(self):
        honey_mass = self.honey_mass
        if honey_mass > 0:
            return sum([item.to_c*(item.mass/honey_mass) for item in self.honey_items])
        else:
            return None

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
    def warm_items(self):
        return WarmItem.objects.filter(recipe=self)

    @property
    def cool_items(self):
        return CoolItem.objects.filter(recipe=self)

    @property
    def water_items(self):
        return list(self.warm_items) + list(self.cool_items)

    @property
    def water_mass(self):
        return sum([item.mass for item in self.water_items])

    @property
    def water_volume(self):
        return sum([item.volume for item in self.water_items])

    @property
    def water_tempC(self):
        water_mass = self.water_mass
        if water_mass > 0:
            return sum([item.to_c*(item.mass/water_mass) for item in self.water_items])
        else:
            return None

    @property
    def water_sg(self):
        water_mass = self.water_mass
        if water_mass > 0:
            return sum([item.water.sg*(item.mass/water_mass) for item in self.water_items])
        else:
            return None

    @property
    def water_sh(self):
        water_mass = self.water_mass
        if water_mass > 0:
            return sum([item.water.sh*(item.mass/water_mass) for item in self.water_items])
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
        return self.honey_mass + self.water_mass

    @property
    def brew_volume(self):
        return self.honey_volume + self.water_volume

    @property
    def brew_sg(self):
        # SG of total is total mass divided by total volume.
        if self.brew_volume > 0:
            return Decimal(self.brew_mass/self.brew_volume).quantize(Decimal('0.001'))
        else:
            return Decimal('0.000')

    @property
    def brew_temp(self):
        water_heat = self.water_tempC * self.water_mass * self.water_sh
        honey_heat = self.honey_tempC * self.honey_mass * self.honey_sh
        total_heat = water_heat + honey_heat
        total_heat_capacity = water_heat/self.water_tempC + honey_heat/self.honey_tempC
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
        water_is_natural = all([item.water.is_natural for item in self.water_items])
        if len(self.flavor_items) > 0:
            flavor_is_natural = all([item.flavor.is_natural for item in self.flavor_items])
        else:
            flavor_is_natural = True
        return honey_is_natural and water_is_natural and flavor_is_natural

    def appellation(self):
        # Proper implementation of appellation testing is very complex.  See 27 CFR 4.25(b) for more information.
        honey_apps = [item.honey.appellation for item in self.honey_items]
        water_apps = [item.water.appellation for item in self.water_items]
        flavor_apps = [item.flavor.appellation for item in self.flavor_items]

        total_apps = set(honey_apps + water_apps + flavor_apps)
        if len(total_apps) == 1:
            return total_apps.pop()
        else:
            return None

    def suggested_category(self):
        honey_types = set([item.honey.type for item in self.honey_items])
        water_types = set([item.water.type for item in self.water_items])
        flavor_types = set([item.flavor.type for item in self.flavor_items])

        # Identify based on honey.
        mead_type = {}
        if Honey.HONEY not in honey_types:
            # Honey is required!
            return None
        if len(honey_types) == 1:
            mead_type['honey'] = MEAD_CATEGORIES['dry']
        elif len(honey_types) == 2:
            if Honey.MALT in honey_types:
                mead_type['honey'] = MEAD_CATEGORIES['braggot']
            elif Honey.OTHER in honey_types:
                mead_type['honey'] = MEAD_CATEGORIES['open_category']
            else:
                # Unknown honey type!
                return None
        else:
            mead_type['honey'] = MEAD_CATEGORIES['open_category']

        # Identify based on water.
        if len(water_types) == 1:
            if Water.WATER in water_types:
                mead_type['water'] = MEAD_CATEGORIES['dry']
            elif Water.APPLE_JUICE in water_types:
                mead_type['water'] = MEAD_CATEGORIES['cyser']
            elif Water.GRAPE_JUICE in water_types:
                mead_type['water'] = MEAD_CATEGORIES['pyment']
            elif Water.FRUIT_JUICE in water_types:
                mead_type['water'] = MEAD_CATEGORIES['other_fruit_melomel']
            elif Water.OTHER in water_types:
                mead_type['water'] = MEAD_CATEGORIES['open_category']
            else:
                # Unknown water type!
                return None
        elif len(water_types) > 1:
            if Water.WATER in water_types:
                if Water.APPLE_JUICE in water_types:
                    mead_type['water'] = MEAD_CATEGORIES['cyser']
                elif Water.GRAPE_JUICE in water_types:
                    mead_type['water'] = MEAD_CATEGORIES['pyment']
                elif Water.FRUIT_JUICE in water_types:
                    mead_type['water'] = MEAD_CATEGORIES['other_fruit_melomel']
                elif Water.OTHER in water_types:
                    mead_type['water'] = MEAD_CATEGORIES['open_category']
                else:
                    # Unknown water type!
                    return None
            else:
                # JMT: no check on unknown water types here
                mead_type['water'] = MEAD_CATEGORIES['open_category']
        else:
            # We need a water type!
            return None

        # Identify based on flavor.
        if len(flavor_types) == 1:
            if Flavor.SPICE in flavor_types:
                mead_type['flavor'] = MEAD_CATEGORIES['metheglin']
            elif Flavor.APPLE in flavor_types:
                mead_type['flavor'] = MEAD_CATEGORIES['cyser']
            elif Flavor.GRAPE in flavor_types:
                mead_type['flavor'] = MEAD_CATEGORIES['pyment']
            elif Flavor.FRUIT in flavor_types:
                mead_type['flavor'] = MEAD_CATEGORIES['other_fruit_melomel']
            elif Flavor.OTHER in flavor_types:
                mead_type['flavor'] = MEAD_CATEGORIES['open_category']
        elif len(flavor_types) > 1:
            mead_type['flavor'] = MEAD_CATEGORIES['open_category']
        else:
            mead_type['flavor'] = MEAD_CATEGORIES['dry']

        # Identify based on all together.
        recipe_type = set(mead_type.values())
        recipe_type.discard(MEAD_CATEGORIES['dry'])
        if len(recipe_type) == 0:
            return MEAD_CATEGORIES['dry']
        if len(recipe_type) == 1:
            return recipe_type.pop()
        else:
            return MEAD_CATEGORIES['open_category']


class Batch(Recipe):
    """
    Batches are actual implementations of recipes.

    Products can be created from batches.
    """

    recipe = models.ForeignKey(Recipe, related_name='source', null=True, on_delete=models.SET_NULL)
    brewname = models.CharField('Brew Name', max_length=8, help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')
    # Used for labels!
    event = models.CharField('Brewing event', max_length=20, help_text='Brewing event (e.g., Lughnasadh 2013, Samhain 2012, Imbolc 2011, Beltane 2010)')
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
                return Decimal(Decimal('100')*(firstsg - lastsg)/Decimal('0.75')).quantize(Decimal('0.01'))
            else:
                return None
        else:
            return None


class Sample(models.Model):
    """ Samples are small collections of data. """
    batch = models.ForeignKey(Batch)
    date = models.DateField()
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
        return Decimal(self.sg + Decimal(str(Sample.deltasg[tempC]))).quantize(Decimal('0.001'))


class ActiveProductManager(models.Manager):
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    def all(self):
        return super(FeaturedProductManager, self).all().filter(is_active=True).filter(is_featured=True)


class InStockProductManager(models.Manager):
    def get_query_set(self):
        return super(InStockProductManager, self).get_query_set().filter(is_active=True, jar__is_active=True, jar__is_available=True).distinct()


class Product(models.Model):
    """
     base class for products.

    """
    brewname = models.CharField('Brew Name', max_length=8, help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')
    slug = models.SlugField(max_length=255, blank=True, unique=True,
                            help_text='Unique value for product page URL, created from brewname and batchletter.')
    title = models.CharField(max_length=40, help_text='Recipe title')
    description = models.TextField(help_text='Description of product.')
    category = models.IntegerField(choices=MEAD_CHOICES, default=MEAD_CATEGORIES['dry'])
    image = models.ImageField(upload_to='images/products/main', blank=True)
    thumbnail = models.ImageField(upload_to='images/products/thumbnails', blank=True)
    is_active = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    brewed_date = models.DateField()
    brewed_sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'))

    bottled_date = models.DateField()
    bottled_sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'))

    abv = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('00.00'))

    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()
    instock = InStockProductManager()

    @property
    def name(self):
        return '%s %s' % (self.brewname, self.batchletter)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-is_active', '-created_at']

    # FIXME: these two have the same magic, need to remove duplication
    def jars_in_stock(self):
        from inventory.models import Jar
        return Jar.instock.filter(product_id=self.pk).count()

    def first_available(self):
        from inventory.models import Jar
        try:
            return Jar.instock.filter(product_id=self.pk).order_by('number')[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('meadery_product', kwargs={'product_slug': self.slug})

    def cross_sells_hybrid(self):
        from checkout.models import Order, OrderItem
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(Q(order__in=orders) |
                                         Q(order__user__in=users)
                                         ).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products


class ActiveProductReviewManager(models.Manager):
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)


class ProductReview(models.Model):
    RATINGS = ((5, '5 - Outstanding'),
               (4, '4 - Excellent'),
               (3, '3 - Very Good'),
               (2, '2 - Good'),
               (1, '1 - Fair'), )
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()

    objects = models.Manager()
    approved = ActiveProductReviewManager()
