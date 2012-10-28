from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

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
    ORDER_STATUSES = ((SUBMITTED,'Submitted'),
                      (PROCESSED,'Processed'),
                      (DELIVERED,'Delivered'),
                      (CANCELLED,'Cancelled'))
    # order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return 'Order #' + str(self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('order_details', (), { 'order_id': self.id })
    
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
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()

