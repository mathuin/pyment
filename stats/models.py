from django.db import models
from django.contrib.auth.models import User
from meadery.models import NewProduct


class PageView(models.Model):
    class Meta:
        abstract = True

    date = models.DateTimeField(auto_now=True)
    ip_address = models.IPAddressField()
    user = models.ForeignKey(User, null=True)
    tracking_id = models.CharField(max_length=50, default='')


class NewProductView(PageView):
    product = models.ForeignKey(NewProduct)
