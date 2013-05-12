from django.contrib import admin
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, NewJar
from inventory.forms import WarehouseAdminForm, RowAdminForm, ShelfAdminForm, BinAdminForm, CrateAdminForm, NewJarAdminForm
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class WarehouseAdmin(admin.ModelAdmin):
    form = WarehouseAdminForm
    list_display = ('name', 'link_rows', 'location',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['number']
    search_fields = ['number', 'location']
    readonly_fields = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('number',)}

    def link_rows(self, obj):
        howmany = obj.rows
        anchor = '%s?warehouse__id__exact=%d' % (reverse('admin:inventory_row_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_rows.short_description = 'Rows'

admin.site.register(Warehouse, WarehouseAdmin)


class RowAdmin(admin.ModelAdmin):
    form = RowAdminForm
    list_display = ('name', 'link_shelves',)
    list_display_links = ('name',)
    list_filter = ('warehouse',)
    list_per_page = 50
    ordering = ['warehouse', 'number']
    readonly_fields = ('created_at', 'updated_at',)

    def link_shelves(self, obj):
        howmany = obj.shelves
        anchor = '%s?row__id__exact=%d' % (reverse('admin:inventory_shelf_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_shelves.short_description = 'Shelves'

admin.site.register(Row, RowAdmin)


class ShelfAdmin(admin.ModelAdmin):
    form = ShelfAdminForm
    list_display = ('name', 'link_bins',)
    list_display_links = ('name',)
    list_filter = ('row__warehouse', 'row',)
    list_per_page = 50
    ordering = ['row__warehouse', 'row', 'number']
    readonly_fields = ('created_at', 'updated_at',)

    def link_bins(self, obj):
        howmany = obj.bins
        anchor = '%s?shelf__id__exact=%d' % (reverse('admin:inventory_bin_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_bins.short_description = 'Bins'

admin.site.register(Shelf, ShelfAdmin)


class BinAdmin(admin.ModelAdmin):
    form = BinAdminForm
    list_display = ('name', 'capacity', 'link_crates',)
    list_display_links = ('name',)
    list_filter = ('shelf__row__warehouse', 'shelf__row', 'shelf',)
    list_per_page = 50
    ordering = ['shelf__row__warehouse', 'shelf__row', 'shelf', 'number']
    readonly_fields = ('created_at', 'updated_at',)

    def link_crates(self, obj):
        howmany = obj.crates
        anchor = '%s?bin__id__exact=%d' % (reverse('admin:inventory_crate_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_crates.short_description = 'Crates'

admin.site.register(Bin, BinAdmin)


class CrateAdmin(admin.ModelAdmin):
    form = CrateAdminForm
    list_display = ('name', 'bin', 'capacity', 'link_jars',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['bin', 'number']
    search_fields = ['number']
    readonly_fields = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('number',)}

    def link_jars(self, obj):
        howmany = obj.jars
        anchor = '%s?crate__id__exact=%d' % (reverse('admin:inventory_jar_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_jars.short_description = 'Jars'

admin.site.register(Crate, CrateAdmin)


class NewJarAdmin(admin.ModelAdmin):
    form = NewJarAdminForm
    list_display = ('product', 'number', 'is_active', 'is_available', 'crate',)
    list_display_links = ('number',)
    list_filter = ('product', 'crate', 'is_active')
    list_per_page = 50
    ordering = ['-created_at', 'is_active']
    search_fields = ['product', 'crate']
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(NewJar, NewJarAdmin)
