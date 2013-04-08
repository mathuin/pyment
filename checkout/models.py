from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from inventory.models import Jar


class BaseOrderInfo(models.Model):
    class Meta:
        abstract = True

    #contact info
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)


class Order(BaseOrderInfo):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    DELIVERED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (DELIVERED, 'Delivered'),
                      (CANCELLED, 'Cancelled'))
    # order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)

    @property
    def name(self):
        return 'Order #' + str(self.id)

    def __unicode__(self):
        return u'%s' % (self.name,)

    @models.permalink
    def get_absolute_url(self):
        return ('order_details', (), {'order_id': self.id})

    def printstatus(self):
        # FIXME: ugly
        return [mystr for (val, mystr) in self.ORDER_STATUSES if val == self.status][0]


class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order)

    @property
    def name(self):
        return self.product.name

    @property
    def title(self):
        return self.product.title

    def __unicode__(self):
        return self.product.title + ' (' + self.product.name + ')'

    @models.permalink
    def get_absolute_url(self):
        return self.product.get_absolute_url()


class PickList(models.Model):
    """A picklist consists of the items to be picked to fulfill a single order."""
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    CANCELLED = 4
    # set of possible order statuses
    PICKLIST_STATUSES = ((SUBMITTED, 'Submitted'),
                         (PROCESSED, 'Processed'),
                         (CANCELLED, 'Cancelled'))

    order = models.ForeignKey(Order)
    status = models.IntegerField(choices=PICKLIST_STATUSES, default=SUBMITTED)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return 'Pick List #' + str(self.id)

    def __unicode__(self):
        return u'%s' % (self.name,)

    @models.permalink
    def get_absolute_url(self):
        return ('picklist_details', (), {'picklist_id': self.id})


class PickListItem(models.Model):
    """A picklist item consists of the jar that is being picked.  The jar contains its name and location."""
    picklist = models.ForeignKey(PickList)
    jar = models.ForeignKey(Jar)

    @property
    def name(self):
        return self.jar.name

    @property
    def bin(self):
        return self.jar.crate.bin.name

    @property
    def crate(self):
        return self.jar.crate.name

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return self.jar.product.get_absolute_url()
