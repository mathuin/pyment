from django.contrib import admin
from utils.buttonadmin import ButtonAdmin
from models import Order, OrderItem, PickList, PickListItem
from checkout import create_picklist, all_in_stock, process_picklist, cancel_picklist, cancel_order
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(ButtonAdmin):
    list_display = ('__unicode__', 'picklist', 'date', 'status', 'user')
    list_filter = ('status', 'date')
    search_fields = ('email', 'id')
    inlines = [OrderItemInline, ]
    fieldsets = (('Basics', {'fields': ('status', 'email', 'phone')}),)
    actions = ['make_processed', 'make_cancelled']

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

    def process_one(self, request, order=None):
        if order is not None:
            if all_in_stock(order) and create_picklist(order):
                self.message_user(request, 'One order was processed!')
            else:
                self.message_user(request, 'No orders were processed!')
        else:
            return None
    process_one.short_description = 'Process order'

    def make_cancelled(self, request, queryset):
        orders_cancelled = 0
        for order in queryset:
            if cancel_order(order):
                orders_cancelled += 1
        if orders_cancelled == 0:
            self.message_user(request, 'No orders were cancelled!')
        else:
            if orders_cancelled == 1:
                self.message_user(request, 'One order was cancelled!')
            else:
                self.message_user(request, '%d orders were cancelled!' % orders_cancelled)
    make_cancelled.short_description = 'Cancel order'

    def cancel_one(self, request, order=None):
        if order is not None:
            if cancel_order(order):
                self.message_user(request, 'One order was cancelled!')
            else:
                self.message_user(request, 'No orders were cancelled!')
        else:
            return None
    cancel_one.short_description = 'Cancel order'

    change_buttons = [process_one, cancel_one]

    # FIXME: add a manager that excludes cancelled orders?
    def picklist(self, obj):
        if PickList.objects.exclude(status=Order.CANCELLED).filter(order=obj).exists():
            mylist = PickList.objects.exclude(status=Order.CANCELLED).get(order=obj)
            return mark_safe('<a href="%s">%s</a>' % (reverse('admin:checkout_picklist_change', args=(mylist.id,)), mylist.name))
        else:
            return ''

admin.site.register(Order, OrderAdmin)


class PickListItemInline(admin.TabularInline):
    model = PickListItem
    extra = 0
    list_display = ('jar', 'crate', 'bin')
    readonly_fields = ('jar', 'crate', 'bin')


class PickListAdmin(ButtonAdmin):
    list_display = ('__unicode__', 'link_order', 'date', 'status')
    inlines = [PickListItemInline, ]
    actions = ['make_processed', 'make_cancelled']
    readonly_fields = ('order',)

    def make_processed(self, request, queryset):
        picklists_processed = 0
        for picklist in queryset:
            if (process_picklist(picklist)):
                picklists_processed += 1
        if picklists_processed == 0:
            self.message_user(request, 'No picklists were processed!')
        else:
            if picklists_processed == 1:
                self.message_user(request, 'One picklist was processed!')
            else:
                self.message_user(request, '%d picklists were processed!' % picklists_processed)
    make_processed.short_description = 'Process picklist'

    def process_one(self, request, picklist=None):
        if picklist is not None:
            if process_picklist(picklist):
                self.message_user(request, '%s was processed!' % picklist.name)
            else:
                self.message_user(request, '%s was not processed!' % picklist.name)
        else:
            return None
    process_one.short_description = 'Process picklist'

    def make_cancelled(self, request, queryset):
        picklists_cancelled = 0
        for picklist in queryset:
            if (cancel_picklist(picklist)):
                picklists_cancelled += 1
        if picklists_cancelled == 0:
            self.message_user(request, 'No picklists were cancelled!')
        else:
            if picklists_cancelled == 1:
                self.message_user(request, 'One picklist was cancelled!')
            else:
                self.message_user(request, '%d picklists were cancelled!' % picklists_cancelled)
    make_cancelled.short_description = 'Cancel picklist'

    def cancel_one(self, request, picklist=None):
        if picklist is not None:
            if cancel_picklist(picklist):
                self.message_user(request, '%s was cancelled!' % picklist.name)
            else:
                self.message_user(request, '%s was not cancelled!' % picklist.name)
        else:
            return None
    cancel_one.short_description = 'Cancel picklist'

    change_buttons = [process_one, cancel_one]

    def link_order(self, obj):
        myorder = obj.order
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:checkout_order_change', args=(myorder.pk,)), myorder.name))
    link_order.short_description = 'Order'

admin.site.register(PickList, PickListAdmin)
