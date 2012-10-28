from django.db import models
from checkout.models import Order
from inventory.models import Jar

class PickList(models.Model):
    """A picklist consists of the items to be picked to fulfill a single order."""
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    CANCELLED = 4
    # set of possible order statuses
    PICKLIST_STATUSES = ((SUBMITTED,'Submitted'),
                         (PROCESSED,'Processed'),
                         (CANCELLED,'Cancelled'))

    order = models.ForeignKey(Order)
    status = models.IntegerField(choices=PICKLIST_STATUSES, default=SUBMITTED)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Pick List #' + str(self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('picklist_details', (), { 'picklist_id': self.id })

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