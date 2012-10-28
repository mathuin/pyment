from django.contrib import admin
from models import PickList, PickListItem
from picklist import process_picklist, cancel_picklist

class PickListItemInline(admin.TabularInline):
    model = PickListItem
    extra = 0
    list_display = ('jar', 'crate', 'bin')
    readonly_fields = ('jar', 'crate', 'bin')
    
class PickListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date', 'status')
    inlines = [PickListItemInline,]
    actions = ['make_processed', 'make_cancelled']
    
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
        
admin.site.register(PickList, PickListAdmin)