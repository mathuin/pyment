from django.contrib import admin
from utils.modeladmin import SmarterModelAdmin
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar
from inventory.forms import WarehouseAdminForm, RowAdminForm, ShelfAdminForm, BinAdminForm, CrateAdminForm, JarAdminForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms
from django.db.models import F, Sum, Case, When, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import render


class WarehouseAdmin(admin.ModelAdmin):
    form = WarehouseAdminForm
    list_display = ('name', 'link_rows', 'location',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['number']
    search_fields = ['number', 'location']
    readonly_fields = ('created_at', 'updated_at',)

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

    def link_jars(self, obj):
        howmany = obj.jars
        anchor = '%s?crate__id__exact=%d' % (reverse('admin:inventory_jar_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_jars.short_description = 'Jars'


admin.site.register(Crate, CrateAdmin)


class JarAdmin(SmarterModelAdmin):
    valid_lookups = ('product',)
    form = JarAdminForm
    list_display = ('product', 'number', 'is_active', 'is_available', 'crate',)
    list_display_links = ('number',)
    list_filter = ('product', 'crate', 'is_active')
    list_per_page = 50
    ordering = ['-created_at', 'is_active']
    search_fields = ['product', 'crate']
    readonly_fields = ('created_at', 'updated_at',)
    actions = ['move_multiple_jars']

    class MoveMultipleJarsForm(forms.Form):
        dest = forms.ModelChoiceField(Crate.objects.none())

        def __init__(self, *args, **kwargs):
            count = kwargs.pop('count')
            super().__init__(*args, **kwargs)
            self.fields['dest'].queryset = Crate.objects.annotate(room=F('capacity')-Sum(Case(When(jar__is_active=True, then=1), default=0), output_field=IntegerField())).filter(room__gte=count).order_by('number')


    def move_multiple_jars(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.MoveMultipleJarsForm(request.POST)

            if form.is_valid():
                dest = form.cleaned_data['dest']

                count = 0
                for jar in queryset:
                    jar.crate = dest
                    jar.save()
                    count += 1

                plural = ''
                if count != 1:
                    plural = 's'

                self.message_user(request, "Successfully moved %d jar%s to %s" % (count, plural, dest))
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.MoveMultipleJarsForm(count=queryset.count())

        return render(request, 'admin/move_multiple_jars.djhtml', {
            'jars': queryset,
            'move_multiple_jars_form': form,
            })

    move_multiple_jars.short_description = "Move multiple jars to new crate"


admin.site.register(Jar, JarAdmin)
