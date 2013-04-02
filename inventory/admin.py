from django.contrib import admin
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar
from inventory.forms import WarehouseAdminForm, RowAdminForm, ShelfAdminForm, BinAdminForm, CrateAdminForm, JarAdminForm


class WarehouseAdmin(admin.ModelAdmin):
    form = WarehouseAdminForm
    list_display = ('name', 'rows', 'location',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['number']
    search_fields = ['number', 'location']
    readonly_fields = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('number',)}

admin.site.register(Warehouse, WarehouseAdmin)


class RowAdmin(admin.ModelAdmin):
    form = RowAdminForm
    list_display = ('name', 'shelves',)
    list_display_links = ('name',)
    list_filter = ('warehouse',)
    list_per_page = 50
    ordering = ['warehouse', 'number']
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Row, RowAdmin)


class ShelfAdmin(admin.ModelAdmin):
    form = ShelfAdminForm
    list_display = ('name', 'bins',)
    list_display_links = ('name',)
    list_filter = ('row__warehouse', 'row',)
    list_per_page = 50
    ordering = ['row__warehouse', 'row', 'number']
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Shelf, ShelfAdmin)


class BinAdmin(admin.ModelAdmin):
    form = BinAdminForm
    list_display = ('name', 'capacity', 'crates',)
    list_display_links = ('name',)
    list_filter = ('shelf__row__warehouse', 'shelf__row', 'shelf',)
    list_per_page = 50
    ordering = ['shelf__row__warehouse', 'shelf__row', 'shelf', 'number']
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Bin, BinAdmin)


class CrateAdmin(admin.ModelAdmin):
    form = CrateAdminForm
    list_display = ('name', 'bin', 'capacity', 'jars',)  # contents? count?
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['bin', 'number']
    search_fields = ['number']
    readonly_fields = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('number',)}

admin.site.register(Crate, CrateAdmin)


class JarAdmin(admin.ModelAdmin):
    form = JarAdminForm
    list_display = ('product', 'number', 'is_active', 'is_available', 'crate',)
    list_display_links = ('number',)
    list_filter = ('product', 'crate')
    list_per_page = 50
    ordering = ['product', 'number', 'crate']
    search_fields = ['product', 'crate']
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Jar, JarAdmin)
