from django.contrib import admin
from models import Order, OrderItem
from checkout import create_picklist, all_in_stock
    
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','date','status','user')
    list_filter = ('status','date')
    search_fields = ('email','id')
    inlines = [OrderItemInline,]
    fieldsets = (('Basics', {'fields': ('status','email','phone')}),)
    actions = ['make_processed']

    def make_processed(self, request, queryset):
        orders_processed = 0
        for order in queryset:
            # do not create picklists unless all products are in stock
            if (all_in_stock(order) and create_picklist(order)):
                orders_processed += 1
        if orders_processed == 0:
            self.message_user(request, 'No orders were processed!')
        else:
            if orders_processed == 1:
                self.message_user(request, 'One order was processed!')
            else:
                self.message_user(request, '%d orders were processed!' % orders_processed)
    make_processed.short_description = 'Process order by making pick list'
    
admin.site.register(Order, OrderAdmin)
