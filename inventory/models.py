from django.db import models
from catalog.models import Product
from django.core.exceptions import ValidationError

# Create your models here.
class Warehouse(models.Model):
    number = models.IntegerField()
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for warehouse page URL, created from name.')
    location = models.TextField()
    # "is_active" means that stuff can be retrieved from it via the normal interface
    # the admin interface can do what it wants
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['number']
    
    @property
    def rows(self):
        return Row.objects.filter(warehouse__id=self.pk, is_active=True).count()
    
    @property
    def name(self):
        return u"Warehouse %d" % self.number
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return('inventory_warehouse', (), { 'warehouse_slug': self.slug })

class Row(models.Model):
    warehouse = models.ForeignKey(Warehouse)
    number = models.IntegerField()
    slug = models.SlugField(max_length=55, blank=True,
                            help_text='Unique value for this row page URL.')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['number']
        unique_together = ('warehouse', 'number')
        
    @property
    def shelves(self):
        return Shelf.objects.filter(row__id=self.pk, is_active=True).count()
    
    @property
    def name(self):
        return u"Row %d in %s" % (self.number, self.warehouse)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = str(self.warehouse.slug)
        super(Row, self).save(*args, **kwargs)
        self.slug = str(self.warehouse.slug) + '-' + str(self.number)
        super(Row, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return('inventory_row', (), { 'row_slug': self.slug })

class Shelf(models.Model):
    row = models.ForeignKey(Row)
    number = models.IntegerField()
    slug = models.SlugField(max_length=60, blank=True,
                            help_text='Unique value for this shelf page URL.')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['number']
        unique_together = ('row', 'number')
        verbose_name_plural = 'Shelves'

    @property        
    def warehouse(self):
        return self.row.warehouse
    
    @property
    def bins(self):
        return Bin.objects.filter(shelf__id=self.pk, is_active=True).count()
    
    @property
    def name(self):
        return u"Shelf %d in %s" % (self.number, self.row)
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = str(self.row.slug)
        super(Shelf, self).save(*args, **kwargs)
        self.slug = str(self.row.slug) + '-' + str(self.number)
        super(Shelf, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return('inventory_shelf', (), { 'shelf_slug': self.slug })
    
class Bin(models.Model):
    shelf = models.ForeignKey(Shelf)
    # must be unique within the shelf
    number = models.IntegerField()
    slug = models.SlugField(max_length=65, blank=True,
                            help_text='Unique value for this bin page URL.')
    # how many crates can fit in this bin
    capacity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['number']
        unique_together = ('shelf', 'number')
        
    @property
    def warehouse(self):
        return self.shelf.row.warehouse
    
    @property
    def row(self):
        return self.shelf.row
    
    @property
    def crates(self):
        return Crate.objects.filter(bin__id=self.pk, is_active=True).count()
    
    @property
    def name(self):
        return u"Bin %d on %s" % (self.number, self.shelf)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = str(self.shelf.slug)
        super(Bin, self).save(*args, **kwargs)
        self.slug = str(self.shelf.slug) + '-' + str(self.number)
        super(Bin, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return('inventory_bin', (), { 'bin_slug': self.slug })

    def clean(self):
        # ensure that the current number of crates is less than or equal to the capacity
        if Crate.objects.filter(bin__id=self.pk, is_active=True).count() > self.capacity:
            raise ValidationError('Capacity of bin exceeded')
          
class Crate(models.Model):
    number = models.IntegerField()
    slug = models.SlugField(max_length=10, unique=True, blank=True)
    capacity = models.IntegerField(default=12)
    # bin where the crate can currently be found
    bin = models.ForeignKey(Bin)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['bin']

    @property
    def name(self):
        return u"Crate %d" % self.number
    
    @property
    def jars(self):
        return Jar.objects.filter(crate__id=self.pk, is_active=True).count()
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return('inventory_crate', (), { 'crate_slug': self.slug })

    def clean(self):
        # ensure that the current number of jars is less than or equal to the capacity
        if self.jars > self.capacity:
            raise ValidationError('Capacity of crate exceeded')
          
class Jar(models.Model):
    product = models.ForeignKey(Product)
    number = models.IntegerField()
    slug = models.SlugField(max_length=13, unique=True, blank=True)
    # volume in liters
    volume = models.IntegerField(default=1)
    crate = models.ForeignKey(Crate)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['crate']
        unique_together = ('product', 'number')

    @property
    def name(self):
        return u"%s%d" % (self.product, self.number)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = str(self.product.slug)
        super(Jar, self).save(*args, **kwargs)
        self.slug = str(self.product.slug) + str(self.number)
        super(Jar, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return('inventory_jar', (), { 'jar_slug': self.slug })
