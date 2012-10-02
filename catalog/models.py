from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
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

    class Meta:
        ordering = ['bjcptag']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name
    
    @property
    def products(self):
        return Product.objects.filter(category__id=self.pk, is_active=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('catalog_category', (), { 'category_slug': self.slug })
    
class Product(models.Model):
    # need clever way to say that 
    brewname = models.CharField('Brew Name', max_length=8,
                                help_text='Unique value for brew name (e.g., SIP 99)')
    batchletter = models.CharField('Batch Letter', max_length=1, help_text='Letter corresponding to batch (e.g., A)')
    slug = models.SlugField(max_length=255, blank=True, unique=True,
                            help_text='Unique value for product page URL, created from brewname and batchletter.')
    title = models.CharField(max_length=255, help_text='Title of batch (e.g., Chocolate With Mint)')
    #brand = models.CharField(max_length=50)
    #sku = models.CharField(max_length=50)
    #price = models.DecimalField(max_digits=9,decimal_places=2)
    #old_price = models.DecimalField(max_digits=9,decimal_places=2,
    #                                blank=True,default=0.00)
    # label
    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    # popular?
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    # flavor text
    description = models.TextField()
    # brewed date and SG
    brewed_date = models.DateField(help_text='Date product was brewed')
    brewed_sg = models.DecimalField(max_digits=4, decimal_places=3, 
                                    help_text='Specific Gravity when product was brewed')
    # bottled date and SG
    bottled_date = models.DateField(help_text='Date product was bottled')
    bottled_sg = models.DecimalField(max_digits=4, decimal_places=3,
                                     help_text='Specific Gravity when product was bottled')
    # status, expected bottling date, expected drinkability date?

    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ugh, does not work here for me
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ['brewname', 'batchletter']

    @property
    def name(self):
        return '%s %s' % (self.brewname, self.batchletter)
    
    @property
    def jars(self):
        from inventory.models import Jar
        return Jar.objects.filter(product__id=self.pk, crate__is_active=True, crate__bin__is_active=True, crate__bin__shelf__is_active=True, crate__bin__shelf__row__is_active=True, crate__bin__shelf__row__warehouse__is_active=True).count()

    @property
    def quantity(self):
        return self.jars.count()

    def __unicode__(self):
        return self.name
           
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), { 'product_slug': self.slug })

    #def sale_price(self):
    #    if self.old_price > self.price:
    #        return self.price
    #    else:
    #        return None

    def abv(self):
        if (self.brewed_sg and self.bottled_sg):
            return 100*((self.brewed_sg-self.bottled_sg)/0.75)
        else:
            return None
