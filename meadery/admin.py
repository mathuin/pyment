from django.contrib import admin
from utils.buttonadmin import ButtonAdmin
from .models import Honey, Water, Flavor, Yeast, HoneyItem, CoolItem, WarmItem, FlavorItem, YeastItem, Recipe, Batch, Sample
from .forms import HoneyAdminForm, WaterAdminForm, FlavorAdminForm, YeastAdminForm, RecipeAdminForm, BatchAdminForm, SampleAdminForm
from meadery import create_batch_from_recipe, create_recipe_from_batch
from django.core.urlresolvers import reverse
from decimal import Decimal


class HoneyAdmin(admin.ModelAdmin):
    form = HoneyAdminForm
    list_display = ('name', 'is_natural', 'appellation', 'sg', 'sh')
    list_display_links = ('name',)
    list_filter = ('is_natural', 'appellation')

admin.site.register(Honey, HoneyAdmin)


class WaterAdmin(admin.ModelAdmin):
    form = WaterAdminForm
    list_display = ('name', 'is_natural', 'appellation', 'sg', 'sh')
    list_display_links = ('name',)
    list_filter = ('is_natural', 'appellation')

admin.site.register(Water, WaterAdmin)


class FlavorAdmin(admin.ModelAdmin):
    form = FlavorAdminForm
    list_display = ('name', 'is_natural', 'appellation', 'units')
    list_display_links = ('name',)
    list_filter = ('is_natural', 'appellation')

admin.site.register(Flavor, FlavorAdmin)


class YeastAdmin(admin.ModelAdmin):
    form = YeastAdminForm
    list_display = ('name', 'is_natural', 'appellation', 'tolerance')
    list_display_links = ('name',)
    list_filter = ('is_natural', 'appellation')

admin.site.register(Yeast, YeastAdmin)


class HoneyItemInline(admin.StackedInline):
    model = HoneyItem
    extra = 0


class WarmItemInline(admin.StackedInline):
    model = WarmItem
    extra = 0


class CoolItemInline(admin.StackedInline):
    model = CoolItem
    extra = 0


class FlavorItemInline(admin.StackedInline):
    model = FlavorItem
    extra = 0


class YeastItemInline(admin.StackedInline):
    model = YeastItem
    extra = 0


class RecipeAdmin(ButtonAdmin):
    list_display = ('title', 'description', 'category', 'brew_volume', 'brew_sg', 'final_sg')
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


class BatchAdmin(ButtonAdmin):
    list_display = ('name', 'recipe', 'jars', 'brew_sg', 'final_sg', 'firstsg', 'lastsg')
    list_display_links = ('name', )
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

    def firstsg(self, obj):
        if obj.sample_set.count() > 0:
            return self.sample_set.order_by('date')[0].corrsg
        else:
            return None
    firstsg.short_description = 'Actual OG'

    def lastsg(self, obj):
        if obj.sample_set.count() > 0:
            return self.sample_set.order_by('-date')[0].corrsg
        else:
            return None
    lastsg.short_description = 'Actual FG'

    def create_recipe(self, request, batch=None):
        if batch is not None:
            if create_recipe_from_batch(batch):
                self.message_user(request, 'One recipe was created!')
            else:
                self.message_user(request, 'No recipe was created!')
        else:
            return None
    create_recipe.short_description = 'Create recipe from batch'

    change_buttons = [create_recipe]

admin.site.register(Batch, BatchAdmin)


class SampleAdmin(admin.ModelAdmin):
    form = SampleAdminForm

admin.site.register(Sample, SampleAdmin)
