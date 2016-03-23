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


class Ingredient(models.Model):
    """Ingredients are found in recipes."""

    name = models.CharField('Ingredient Name', max_length=40, help_text='Ingredient name')
    is_natural = models.BooleanField(default=False, help_text='TRUE if the ingredient does not contain added color, artificial flavors, or synthetic substances.')
    # JMT: may need to change appellation to a dropdown list
    appellation = models.CharField('Appellation', max_length=20, help_text='Where the ingredient was made (i.e., Oregon, California, Brazil)')
    # Ingredient types.
    TYPE_SUGAR = 1
    TYPE_SOLVENT = 2
    TYPE_FLAVOR = 3
    TYPE_YEAST = 4
    INGREDIENT_TYPES = ((TYPE_SUGAR, 'Sugar'),
                        (TYPE_SOLVENT, 'Solvent'),
                        (TYPE_FLAVOR, 'Flavor'),
                        (TYPE_YEAST, 'Yeast'))
    type = models.IntegerField(choices=INGREDIENT_TYPES, default=TYPE_SUGAR)
    # Ingredient subtypes.
    SUGAR_HONEY = 101
    SUGAR_MALT = 102
    SUGAR_OTHER = 103
    SUGAR_TYPES = ((SUGAR_HONEY, 'Honey'),
                   (SUGAR_MALT, 'Malt'),
                   (SUGAR_OTHER, 'Other'))
    SOLVENT_WATER = 201
    SOLVENT_GRAPE = 202
    SOLVENT_APPLE = 203
    SOLVENT_FRUIT = 204
    SOLVENT_OTHER = 205
    SOLVENT_TYPES = ((SOLVENT_WATER, 'Water'),
                     (SOLVENT_GRAPE, 'Grape Juice'),
                     (SOLVENT_APPLE, 'Apple Juice'),
                     (SOLVENT_FRUIT, 'Fruit Juice'),
                     (SOLVENT_OTHER, 'Other'))
    FLAVOR_SPICE = 301
    FLAVOR_GRAPE = 302
    FLAVOR_APPLE = 303
    FLAVOR_FRUIT = 304
    FLAVOR_OTHER = 305
    FLAVOR_TYPES = ((FLAVOR_SPICE, 'Spice'),
                    (FLAVOR_GRAPE, 'Grape'),
                    (FLAVOR_APPLE, 'Apple'),
                    (FLAVOR_FRUIT, 'Fruit'),
                    (FLAVOR_OTHER, 'Other'))
    YEAST_DRY = 401
    YEAST_WET = 402
    YEAST_TYPES = ((YEAST_DRY, 'Dry'),
                   (YEAST_WET, 'Wet'))
    INGREDIENT_SUBTYPES = ((TYPE_SUGAR, SUGAR_TYPES),
                           (TYPE_SOLVENT, SOLVENT_TYPES),
                           (TYPE_FLAVOR, FLAVOR_TYPES),
                           (TYPE_YEAST, YEAST_TYPES))
    INGREDIENT_CHOICES = tuple((b, d) for ((a, b), (c, d)) in zip(INGREDIENT_TYPES, INGREDIENT_SUBTYPES))
    subtype = models.IntegerField(choices=INGREDIENT_CHOICES, default=SUGAR_HONEY)
    # Ingredient states.
    STATE_SOLID = 1  # Amount is in kilograms.
    STATE_LIQUID = 2  # Amount is in liters.
    STATE_OTHER = 3  # Amount is in something else.
    INGREDIENT_STATES = ((STATE_SOLID, 'Solid'),
                         (STATE_LIQUID, 'Liquid'),
                         (STATE_OTHER, 'Other'))
    # Certain states are only valid for certain types.
    STATE_TYPES = ((STATE_SOLID, (TYPE_SUGAR, )),
                   (STATE_LIQUID, (TYPE_SOLVENT, )),
                   (STATE_OTHER, (TYPE_FLAVOR, TYPE_YEAST)))

    state = models.IntegerField(choices=INGREDIENT_STATES, default=STATE_SOLID)
    sg = models.DecimalField('Specific Gravity', max_digits=4, decimal_places=3, default=Decimal('1.000'), help_text='Specific gravity (water is 1.000, honey is usually 1.422)')
    sh = models.DecimalField('Specific Heat', max_digits=3, decimal_places=2, default=Decimal('1.00'), help_text='Specific heat (water is 1.00, honey is usually 0.57)')
    tolerance = models.IntegerField('Alcohol tolerance', default=12, help_text='Maximum alcohol tolerance in percent (only for yeast)')
    cpu = models.DecimalField('Cost Per Unit', max_digits=5, decimal_places=2, default=Decimal('1.00'), help_text='Cost in USD per unit (kilogram if solid, liter if liquid, other if other)')

    class Meta:
        ordering = ('state',)

    def __unicode__(self):
        return u'%s' % self.name


class IngredientItem(models.Model):
    parent = models.ForeignKey('Parent')
    ingredient = models.ForeignKey(Ingredient)
    amount = models.DecimalField(max_digits=5, decimal_places=3, help_text='Amount of ingredient (kilograms if solid, liters if liquid, units if other)')
    temp = models.IntegerField(help_text='Temperature of ingredient in degrees Fahrenheit')

    class Meta:
        ordering = ('ingredient', '-temp',)

    @property
    def to_mass(self):
        return Decimal(self.amount * self.sg).quantize(Decimal('0.001'))

    @property
    def to_volume(self):
        return Decimal(self.amount / self.sg).quantize(Decimal('0.001'))

    @property
    def to_c(self):
        return Decimal((self.temp - 32) / 1.8).quantize(Decimal('0.1'))


class ParentManager(models.Manager):
    def contribute_to_class(self, model, name):
        super(ParentManager, self).contribute_to_class(model, name)
        models.signals.pre_save.connect(set_category, model)


def set_category(sender, **kwargs):
    instance = kwargs.pop('instance', False)
    if instance.items() is not []:
        sugar_types = set([item.ingredient.subtype for item in instance.items(Ingredient.TYPE_SUGAR)])
        solvent_types = set([item.ingredient.subtype for item in instance.items(Ingredient.TYPE_SOLVENT)])
        flavor_types = set([item.ingredient.subtype for item in instance.items(Ingredient.TYPE_FLAVOR)])

        instance.category = instance.suggested_category(sugar_types, solvent_types, flavor_types)


class Parent(models.Model):
    CATEGORY_TRADITIONAL = 240
    CATEGORY_MELOMEL = 250
    CATEGORY_OTHER = 260
    CATEGORY_ALL = 290
    MEAD_CATEGORIES = ((CATEGORY_TRADITIONAL, 'Traditional Mead'),
                       (CATEGORY_MELOMEL, 'Melomel'),
                       (CATEGORY_OTHER, 'Other Meads'),
                       (CATEGORY_ALL, 'All Meads'))
    TRADITIONAL_DRY = 241
    TRADITIONAL_SEMI_SWEET = 242
    TRADITIONAL_SWEET = 243
    TRADITIONAL_CATEGORIES = ((TRADITIONAL_DRY, 'Dry Mead'),
                              (TRADITIONAL_SEMI_SWEET, 'Semi-Sweet Mead'),
                              (TRADITIONAL_SWEET, 'Sweet Mead'))
    MELOMEL_CYSER = 251
    MELOMEL_PYMENT = 252
    MELOMEL_OTHER = 253
    MELOMEL_CATEGORIES = ((MELOMEL_CYSER, 'Cyser'),
                          (MELOMEL_PYMENT, 'Pyment'),
                          (MELOMEL_OTHER, 'Other Fruit Melomel'))
    OTHER_METHEGLIN = 261
    OTHER_BRAGGOT = 262
    OTHER_OPEN_CATEGORY = 263
    OTHER_CATEGORIES = ((OTHER_METHEGLIN, 'Metheglin'),
                        (OTHER_BRAGGOT, 'Braggot'),
                        (OTHER_OPEN_CATEGORY, 'Open Category Mead'))
    ALL = 291
    ALL_CATEGORIES = ((ALL, 'All'),)

    MEAD_SUBCATEGORIES = ((CATEGORY_TRADITIONAL, TRADITIONAL_CATEGORIES),
                          (CATEGORY_MELOMEL, MELOMEL_CATEGORIES),
                          (CATEGORY_OTHER, OTHER_CATEGORIES),
                          (CATEGORY_ALL, ALL_CATEGORIES))
    MEAD_CHOICES = tuple((b, d) for ((a, b), (c, d)) in zip(MEAD_CATEGORIES, MEAD_SUBCATEGORIES))
    # JMT: it would be awesome to redo categories to support two levels!
    MEAD_VIEWS = reduce(lambda t1, t2: t1 + t2, [categories for (topvalue, categories) in MEAD_CHOICES])
    MEAD_DESCRIPTIONS = {TRADITIONAL_DRY: 'A traditional mead with subtle honey aroma but no significant aromatics. Minimal residual sweetness with a dry finish, and a light to medium body. Similar to a dry white wine. (Based on BJCP Style Guidelines 2008)',
                         TRADITIONAL_SEMI_SWEET: 'A traditional mead with noticeable honey aroma and subtle to moderate residual sweetness with a medium-dry finish.  Body is medium-light to medium-full.  Similar to a semi-sweet (or medium-dry) white wine.  (thanks to BJCP Style Guidelines 2008)',
                         TRADITIONAL_SWEET: 'A traditional mead with dominating honey aroma, often moderately to strongly sweet.  The body is generally medium-full to full, and may seem like a dessert wine.  (thanks to BJCP Style Guidelines 2008)',
                         MELOMEL_CYSER: 'A mead made from honey and apple juice, with a variety of flavors.  (thanks to BJCP Style Guidelines 2008)',
                         MELOMEL_PYMENT: 'A melomel made from grapes or grape juice.  (thanks to BJCP Style Guidelines 2008)',
                         MELOMEL_OTHER: 'A mead made from honey and fruit (not grapes or apples).  (thanks to BJCP Style Guidelines 2008)',
                         OTHER_METHEGLIN: 'A spiced mead.  (thanks to BJCP Style Guidelines 2008)',
                         OTHER_BRAGGOT: 'A mead made with malt. (thanks to BJCP Style Guidelines 2008)',
                         OTHER_OPEN_CATEGORY: 'A honey-based beverage that either combines ingredients from two or more of the other mead sub-categories, is a historical or indigenous mead (e.g., tej, Polish meads), or is a mead that does not fit into any other category.  Any specialty or experimental mead using additional sources of fermentables (e.g., maple syrup, molasses, brown sugar, or agave nectar), additional ingredients (e.g., vegetables, liquors, smoke, etc.), alternative processes (e.g., icing, oak-aging) or other unusual ingredient, process, or technique would also be appropriate in this category.',
                         ALL: 'Everything in the store!'}

    objects = ParentManager()

    title = models.CharField(max_length=40, help_text='Recipe title')
    description = models.TextField(help_text='Description of product.')
    category = models.IntegerField(choices=MEAD_CHOICES, default=TRADITIONAL_DRY)

    @property
    def name(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title

    def items(self, type=None):
        if type is None:
            return IngredientItem.objects.filter(parent=self)
        else:
            return IngredientItem.objects.filter(parent=self, ingredient__type=type)

    @property
    def all_natural(self):
        # JMT: skipping yeast
        relevant_items = self.items(Ingredient.TYPE_SUGAR) | self.items(Ingredient.TYPE_SOLVENT) | self.items(Ingredient.TYPE_FLAVOR)
        return all([item.ingredient.is_natural for item in relevant_items])

    @property
    def appellation(self):
        # Proper implementation of appellation testing is very complex.
        # See 27 CFR 4.25(b) for more information.
        # JMT: skipping yeast
        relevant_items = self.items(Ingredient.TYPE_SUGAR) | self.items(Ingredient.TYPE_SOLVENT) | self.items(Ingredient.TYPE_FLAVOR)
        total_appellations = set([item.ingredient.appellation for item in relevant_items])
        if len(total_appellations) == 1:
            return total_appellations.pop()
        else:
            return None

    def suggested_category(self, sugar_types, solvent_types, flavor_types):
        # Identify based on sugar.
        mead_type = {}
        if len(sugar_types) == 1:
            mead_type['sugar'] = Parent.TRADITIONAL_DRY
        elif len(sugar_types) == 2:
            if Ingredient.SUGAR_MALT in sugar_types:
                mead_type['sugar'] = Parent.OTHER_BRAGGOT
            else:
                mead_type['sugar'] = Parent.OTHER_OPEN_CATEGORY
        else:
            mead_type['sugar'] = Parent.OTHER_OPEN_CATEGORY

        # Identify based on solvent.
        if len(solvent_types) == 1:
            if Ingredient.SOLVENT_WATER in solvent_types:
                mead_type['solvent'] = Parent.TRADITIONAL_DRY
            elif Ingredient.SOLVENT_APPLE in solvent_types:
                mead_type['solvent'] = Parent.MELOMEL_CYSER
            elif Ingredient.SOLVENT_GRAPE in solvent_types:
                mead_type['solvent'] = Parent.MELOMEL_PYMENT
            elif Ingredient.SOLVENT_FRUIT in solvent_types:
                mead_type['solvent'] = Parent.MELOMEL_OTHER
            else:
                mead_type['solvent'] = Parent.OTHER_OPEN_CATEGORY
        elif len(solvent_types) == 2:
            if Ingredient.SOLVENT_WATER in solvent_types:
                if Ingredient.SOLVENT_APPLE in solvent_types:
                    mead_type['solvent'] = Parent.MELOMEL_CYSER
                elif Ingredient.SOLVENT_GRAPE in solvent_types:
                    mead_type['solvent'] = Parent.MELOMEL_PYMENT
                elif Ingredient.SOLVENT_FRUIT in solvent_types:
                    mead_type['solvent'] = Parent.MELOMEL_OTHER
                else:
                    mead_type['solvent'] = Parent.OTHER_OPEN_CATEGORY
            else:
                mead_type['solvent'] = Parent.OTHER_OPEN_CATEGORY
        else:
            mead_type['solvent'] = Parent.OTHER_OPEN_CATEGORY

        # Identify based on flavor.
        if len(flavor_types) == 0:
            mead_type['flavor'] = Parent.TRADITIONAL_DRY
        elif len(flavor_types) == 1:
            if Ingredient.FLAVOR_SPICE in flavor_types:
                mead_type['flavor'] = Parent.OTHER_METHEGLIN
            elif Ingredient.FLAVOR_APPLE in flavor_types:
                mead_type['flavor'] = Parent.MELOMEL_CYSER
            elif Ingredient.FLAVOR_GRAPE in flavor_types:
                mead_type['flavor'] = Parent.MELOMEL_PYMENT
            elif Ingredient.FLAVOR_FRUIT in flavor_types:
                mead_type['flavor'] = Parent.MELOMEL_OTHER
            elif Ingredient.FLAVOR_OTHER in flavor_types:
                mead_type['flavor'] = Parent.OTHER_OPEN_CATEGORY
        elif len(flavor_types) > 1:
            mead_type['flavor'] = Parent.OTHER_OPEN_CATEGORY

        # Identify based on all together.
        recipe_type = set(mead_type.values())
        recipe_type.discard(Parent.TRADITIONAL_DRY)
        if len(recipe_type) == 0:
            # JMT: add SG calculations here
            return Parent.TRADITIONAL_DRY
        if len(recipe_type) == 1:
            return recipe_type.pop()
        else:
            return Parent.OTHER_OPEN_CATEGORY


class Recipe(Parent):
    pass


class SIPParent(Parent):
    brewname = models.CharField('Brew Name', max_length=8, help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['is_active', '-created_at']

    @property
    def name(self):
        return '%s %s' % (self.brewname, self.batchletter)

    def __unicode__(self):
        return self.name


class Batch(SIPParent):
    recipe = models.ForeignKey(Recipe, blank=True, null=True, on_delete=models.SET_NULL)
    # Used for labels!
    event = models.CharField('Brewing event', max_length=20, help_text='Brewing event (e.g., Lughnasadh 2013, Samhain 2012, Imbolc 2011, Beltane 2010)')
    jars = models.IntegerField(help_text='Number of jars actually produced from this batch.')

    @property
    def abv(self):
        zero = Decimal('0.000')
        if self.sample_set.count() > 1:
            firstsg = self.sample_set.order_by('date')[0].corrsg
            lastsg = self.sample_set.order_by('-date')[0].corrsg
            if firstsg != zero and lastsg != zero and firstsg > lastsg:
                return Decimal(Decimal('100') * (firstsg - lastsg) / Decimal('0.75')).quantize(Decimal('0.01'))
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
               0.0000, 0.0002, 0.0003, 0.0005, 0.0007,
               0.0009, 0.0011, 0.0013, 0.0016, 0.0018,
               0.0021, 0.0023, 0.0026, 0.0029, 0.0032,
               0.0035, 0.0038, 0.0041, 0.0044, 0.0047,
               0.0051, 0.0054, 0.0058, 0.0061, 0.0065,
               0.0069, 0.0073, 0.0077, 0.0081, 0.0085,
               0.0089, 0.0093, 0.0097, 0.0102, 0.0106]

    class Meta:
        ordering = ('date', )

    def __unicode__(self):
        return u'Sample #{0}'.format(self.pk)

    @property
    def corrsg(self):
        # Convert temperature from Fahrenheit to Celsius first.
        tempC = int((self.temp - 32) / 1.8)
        return Decimal(self.sg + Decimal(str(Sample.deltasg[tempC]))).quantize(Decimal('0.001'))


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    def all(self):
        return super(FeaturedProductManager, self).all().filter(is_active=True).filter(is_featured=True)


class InStockProductManager(models.Manager):
    def get_queryset(self):
        return super(InStockProductManager, self).get_queryset().filter(is_active=True, jar__is_active=True, jar__is_available=True).distinct()


class Product(SIPParent):
    slug = models.SlugField(max_length=255, blank=True, unique=True,
                            help_text='Unique value for product page URL, created from brewname and batchletter.')
    image = models.ImageField(upload_to='images/products/main', blank=True)
    thumbnail = models.ImageField(upload_to='images/products/thumbnails', blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')

    brewed_date = models.DateField()
    brewed_sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'))

    bottled_date = models.DateField()
    bottled_sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'))

    abv = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('00.00'))

    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()
    instock = InStockProductManager()

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
