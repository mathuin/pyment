from django.contrib import admin
from utils.buttonadmin import ButtonAdmin
from .models import Honey, Water, Flavor, Yeast, HoneyItem, CoolItem, WarmItem, FlavorItem, YeastItem, Recipe, Batch, Sample
from .forms import HoneyAdminForm, WaterAdminForm, FlavorAdminForm, YeastAdminForm, RecipeAdminForm, BatchAdminForm, SampleAdminForm
from meadery import create_batch_from_recipe, create_recipe_from_batch, create_product_from_batch, make_labels_from_batch
from django.core.urlresolvers import reverse
from decimal import Decimal
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_natural', 'appellation', )
    list_display_links = ('name', )
    list_filter = ('is_natural', 'appellation')


class HoneyAdmin(IngredientAdmin):
    form = HoneyAdminForm
    list_display = IngredientAdmin.list_display + ('sg', 'sh', )

admin.site.register(Honey, HoneyAdmin)


class WaterAdmin(IngredientAdmin):
    form = WaterAdminForm
    list_display = IngredientAdmin.list_display + ('sg', 'sh', )

admin.site.register(Water, WaterAdmin)


class FlavorAdmin(IngredientAdmin):
    form = FlavorAdminForm
    list_display = IngredientAdmin.list_display + ('units', )

admin.site.register(Flavor, FlavorAdmin)


class YeastAdmin(IngredientAdmin):
    form = YeastAdminForm
    list_display = IngredientAdmin.list_display + ('tolerance', )

admin.site.register(Yeast, YeastAdmin)


class IngredientItemInline(admin.StackedInline):
    extra = 0


class HoneyItemInline(IngredientItemInline):
    model = HoneyItem


class WarmItemInline(IngredientItemInline):
    model = WarmItem


class CoolItemInline(IngredientItemInline):
    model = CoolItem


class FlavorItemInline(IngredientItemInline):
    model = FlavorItem


class YeastItemInline(IngredientItemInline):
    model = YeastItem


class RecipeAdmin(ButtonAdmin):
    list_display = ('title', 'description', 'category', 'all_natural', 'appellation', 'brew_volume', 'brew_sg', 'final_sg')
    list_display_links = ('title', )
    inlines = [HoneyItemInline, WarmItemInline, CoolItemInline, FlavorItemInline, YeastItemInline, ]

    def brew_sg(self, obj):
        return obj.brew_sg
    brew_sg.short_description = 'Projected OG'

    def final_sg(self, obj):
        if len(obj.yeast_items) > 0:
            deltasg = max([item.yeast.maxdeltasg for item in obj.yeast_items])
        else:
            deltasg = 0
        return Decimal(obj.brew_sg - deltasg)
    final_sg.short_description = 'Projected FG'

    def create_batch(self, request, recipe=None):
        if recipe is not None:
            if create_batch_from_recipe(recipe):
                self.message_user(request, 'One batch was created!')
            else:
                self.message_user(request, 'No batch was created!')
        else:
            return None
    create_batch.short_description = 'Create batch from recipe'

    change_buttons = [create_batch]


admin.site.register(Recipe, RecipeAdmin)


class BatchAdmin(RecipeAdmin):
    list_display = ('name', 'recipe', 'all_natural', 'appellation', 'brew_sg', 'final_sg', 'link_samples', 'firstsg', 'lastsg', 'abv', 'jars', )
    list_display_links = ('name', )

    def link_samples(self, obj):
        howmany = obj.sample_set.count()
        anchor = '%s?batch=%d' % (reverse('admin:meadery_sample_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_samples.short_description = 'Samples'

    def firstsg(self, obj):
        # if obj.sample_set.count() > 0:
        if Sample.objects.filter(batch=obj).exists():
            return Sample.objects.filter(batch=obj).order_by('date')[0].corrsg
            # return self.sample_set.order_by('date')[0].corrsg
        else:
            return None
    firstsg.short_description = 'Actual OG'

    def lastsg(self, obj):
        # if obj.sample_set.count() > 0:
        if Sample.objects.filter(batch=obj).exists():
            return Sample.objects.filter(batch=obj).order_by('-date')[0].corrsg
            # return self.sample_set.order_by('-date')[0].corrsg
        else:
            return None
    lastsg.short_description = 'Actual FG'

    def abv(self, obj):
        return obj.abv
    abv.short_description = 'Alc. % by vol.'

    def create_recipe(self, request, batch=None):
        if batch is not None:
            if create_recipe_from_batch(batch):
                self.message_user(request, 'One recipe was created!')
            else:
                self.message_user(request, 'No recipe was created!')
        else:
            return None
    create_recipe.short_description = 'Create recipe from batch'

    def create_product(self, request, batch=None):
        if batch is not None:
            if create_product_from_batch(batch):
                self.message_user(request, 'One product was created!')
            else:
                self.message_user(request, 'No product was created!')
        else:
            return None
    create_product.short_description = 'Create product from batch'

    def add_sample(self, request, batch=None):
        if batch is not None:
            return HttpResponseRedirect('%s?batch=%d' % (reverse('admin:meadery_sample_add'), batch.pk))
        else:
            return None
    add_sample.short_description = 'Add sample'

    def make_labels(self, request, batch=None):
        if batch is not None:
            pdf = make_labels_from_batch(batch)
            if pdf is not None:
                self.message_user(request, 'Labels were made for batch {}'.format(batch))
                filename = ''.join([batch.brewname, batch.batchletter]).lower().replace(' ', '')
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(filename)
                response.write(pdf)
                return response
            else:
                self.message_user(request, 'No labels were made!')
        else:
            return None
    make_labels.short_description = 'Make labels'

    change_buttons = [make_labels, add_sample, create_recipe, create_product]

admin.site.register(Batch, BatchAdmin)


class SampleAdmin(admin.ModelAdmin):
    form = SampleAdminForm
    list_display = ('batch', 'date', 'temp', 'sg', 'notes', )
    list_display_links = ('batch', )
    list_filter = ['batch', ]
    ordering = ['batch', 'date']

    def batch(self, obj):
        return obj.batch.name

admin.site.register(Sample, SampleAdmin)
