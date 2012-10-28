from models import PickList, PickListItem
from checkout.models import Order

def process_picklist(self):
    if self.status == PickList.SUBMITTED and self.order.status == Order.PROCESSED:
        # iterate through every jar and make it no longer active
        picklist_items = PickListItem.objects.filter(picklist=self.pk)
        for pli in picklist_items:
            pli.jar.is_active = False
            pli.jar.save()
        self.order.status = Order.DELIVERED
        self.order.save()
        self.status = PickList.PROCESSED
        self.save()
        return True
        
def cancel_picklist(self):
    if self.status == PickList.SUBMITTED and self.order.status == Order.PROCESSED:
        # iterate through every jar and make it available again
        picklist_items = PickListItem.objects.filter(picklist=self.pk)
        for pli in picklist_items:
            pli.jar.is_available = True
            pli.jar.save()           
        self.order.status = Order.SUBMITTED
        self.order.save()
        self.status = PickList.CANCELLED
        self.save()
        return True
    
