from django.db import models
from django import forms
from django.contrib.auth.models import User
from catalog.models import Product

class Order(models.Model):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Submitted'),
                      (PROCESSED,'Processed'),
                      (SHIPPED,'Shipped'),
                      (CANCELLED,'Cancelled'))
    # order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    # contact info
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return 'Order #' + str(self.id)

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

