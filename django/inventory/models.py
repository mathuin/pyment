from django.urls import reverse
from django.db import models
from meadery.models import Product
from django.core.exceptions import ValidationError


class Warehouse(models.Model):
    number = models.IntegerField()
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for warehouse page URL, created from name.')
    location = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    @property
    def rows(self):
        return self.row_set.count()

    @property
    def shortname(self):
        return "W%d" % self.number

    @property
    def longname(self):
        return "Warehouse %d" % self.number

    @property
    def name(self):
        return self.longname

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = 'w%d' % self.number
        super(Warehouse, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory_warehouse', kwargs={'warehouse_slug': self.slug})


class Row(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    number = models.IntegerField()
    slug = models.SlugField(max_length=55, blank=True,
                            help_text='Unique value for this row page URL.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['warehouse', 'number']
        unique_together = ('warehouse', 'number')

    @property
    def shelves(self):
        return self.shelf_set.count()

    @property
    def shortname(self):
        return "%sR%d" % (self.warehouse.shortname, self.number)

    @property
    def longname(self):
        return "%s Row %d" % (self.warehouse.longname, self.number)

    @property
    def name(self):
        return self.longname

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '-'.join([self.warehouse.slug, 'r%d' % self.number])
        super(Row, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory_row', kwargs={'row_slug': self.slug})


class Shelf(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    number = models.IntegerField()
    slug = models.SlugField(max_length=60, blank=True,
                            help_text='Unique value for this shelf page URL.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['row', 'number']
        unique_together = ('row', 'number')
        verbose_name_plural = 'Shelves'

    @property
    def warehouse(self):
        return self.row.warehouse

    @property
    def bins(self):
        return self.bin_set.count()

    @property
    def shortname(self):
        return "%sS%d" % (self.row.shortname, self.number)

    @property
    def longname(self):
        return "%s Shelf %d" % (self.row.longname, self.number)

    @property
    def name(self):
        return self.longname

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '-'.join([self.row.slug, 's%d' % self.number])
        super(Shelf, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory_shelf', kwargs={'shelf_slug': self.slug})


class Bin(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    # must be unique within the shelf
    number = models.IntegerField()
    slug = models.SlugField(max_length=65, blank=True,
                            help_text='Unique value for this bin page URL.')
    # how many crates can fit in this bin
    capacity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['shelf', 'number']
        unique_together = ('shelf', 'number')

    @property
    def warehouse(self):
        return self.shelf.row.warehouse

    @property
    def row(self):
        return self.shelf.row

    @property
    def crates(self):
        return self.crate_set.count()

    @property
    def shortname(self):
        return "%sB%d" % (self.shelf.shortname, self.number)

    @property
    def longname(self):
        return "%s Bin %d" % (self.shelf.longname, self.number)

    @property
    def name(self):
        return self.longname

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '-'.join([self.shelf.slug, 'b%d' % self.number])
        super(Bin, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory_bin', kwargs={'bin_slug': self.slug})

    def clean(self):
        # ensure that the current number of crates is less than or equal to the capacity
        if self.crates > self.capacity:
            raise ValidationError('Capacity of bin exceeded')


class Crate(models.Model):
    number = models.IntegerField()
    slug = models.SlugField(max_length=10, unique=True, blank=True)
    capacity = models.IntegerField(default=12)
    # bin where the crate can currently be found
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    @property
    def jars(self):
        return self.jar_set.filter(is_active=True).count()

    @property
    def shortname(self):
        return "C%d" % self.number

    @property
    def longname(self):
        return "Crate %d" % self.number

    @property
    def name(self):
        return self.longname

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = 'c%d' % self.number
        super(Crate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory_crate', kwargs={'crate_slug': self.slug})

    def clean(self):
        # ensure that the current number of jars is less than or equal to the capacity
        if self.jars > self.capacity:
            raise ValidationError('Capacity of crate exceeded')


class InStockJarManager(models.Manager):
    def get_queryset(self):
        return super(InStockJarManager, self).get_queryset().filter(is_active=True, is_available=True)


class Jar(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField()
    slug = models.SlugField(max_length=13, unique=True, blank=True)
    # volume in liters
    volume = models.IntegerField(default=1)
    crate = models.ForeignKey(Crate, on_delete=models.CASCADE)
    # is_active = not yet sold
    is_active = models.BooleanField(default=True)
    # is_available = considered 'in stock'
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instock = InStockJarManager()

    class Meta:
        ordering = ['created_at']
        unique_together = ('product', 'number')

    @property
    def name(self):
        return "%s%d" % (self.product, self.number)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = ''.join([self.product.slug, str(self.number)])
        super(Jar, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory_jar', kwargs={'jar_slug': self.slug})
