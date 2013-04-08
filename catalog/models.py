from django.db import models
from django.template.defaultfilters import slugify
from decimal import Decimal
from django.contrib.auth.models import User


class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    bjcptag = models.CharField('BJCP Tag', max_length=5, unique=True,
                               help_text='Beer Judge Certification Program style (e.g. 24A)')
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField('Meta Keywords', max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField('Meta Description', max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveCategoryManager()

    class Meta:
        ordering = ['bjcptag']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    @property
    def products(self):
        return self.product_set.filter(is_active=True)

    @property
    def instock(self):
        from inventory.models import Jar
        return Jar.instock.filter(product_id__in=Product.active.filter(pk__in=self.products.values_list('id', flat=True)).values_list('id', flat=True)).exists()

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_category', (), {'category_slug': self.slug})


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
    brewname = models.CharField('Brew Name', max_length=8,
                                help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')
    slug = models.SlugField(max_length=255, blank=True, unique=True,
                            help_text='Unique value for product page URL, created from brewname and batchletter.')
    title = models.CharField(max_length=255, help_text='Title of batch (e.g., Chocolate With Mint)')
    # label
    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    is_active = models.BooleanField(default=True)
    # popular?
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    # flavor text
    description = models.TextField()
    # brewed date and SG
    brewed_date = models.DateField(help_text='Date product was brewed')
    brewed_sg = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'),
                                    help_text='Specific Gravity when product was brewed')
    # bottled date and SG
    bottled_date = models.DateField(help_text='Date product was bottled')
    bottled_sg = models.DecimalField(max_digits=4, decimal_places=3, default=('0.000'),
                                     help_text='Specific Gravity when product was bottled')
    # status, expected bottling date, expected drinkability date?

    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category)

    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()
    instock = InStockProductManager()

    class Meta:
        ordering = ['-is_active', '-created_at']

    @property
    def name(self):
        return '%s %s' % (self.brewname, self.batchletter)

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

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), {'product_slug': self.slug})

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

    @property
    def abv(self):
        zero = Decimal('0.000')
        if (self.brewed_sg != zero and self.bottled_sg != zero and self.brewed_sg > self.bottled_sg):
            return '%0.2f' % (Decimal('100')*(self.brewed_sg - self.bottled_sg)/Decimal('0.75'))
        else:
            return '---'


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
