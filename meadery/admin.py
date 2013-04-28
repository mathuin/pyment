from django.contrib import admin
from utils.buttonadmin import ButtonAdmin
from .models import Honey, Water, Flavor, Yeast, Recipe, Batch, Sample
from .forms import HoneyAdminForm, WaterAdminForm, FlavorAdminForm, YeastAdminForm, RecipeAdminForm, BatchAdminForm, SampleAdminForm
from meadery import create_batch_from_recipe, create_recipe_from_batch
from django.core.urlresolvers import reverse


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
    list_display = ('name', 'is_natural', 'appellation', 'maxdeltasg')
    list_display_links = ('name',)
    list_filter = ('is_natural', 'appellation')

admin.site.register(Yeast, YeastAdmin)


class RecipeAdmin(ButtonAdmin):

    def create_batch(self, request, recipe=None):
        if recipe is not None:
            if create_batch_from_recipe(recipe):
                self.message_user(request, 'One batch was created!')
            else:
                self.message_user(request, 'No batch was created!')
        else:
            return None
    create_batch.short_description = 'Create batch'

    change_buttons = [create_batch]


admin.site.register(Recipe, RecipeAdmin)


class BatchAdmin(ButtonAdmin):

    def create_recipe(self, request, batch=None):
        if batch is not None:
            if create_recipe_from_batch(batch):
                self.message_user(request, 'One recipe was created!')
            else:
                self.message_user(request, 'No recipe was created!')
        else:
            return None
    create_recipe.short_description = 'Create recipe'

    change_buttons = [create_recipe]

admin.site.register(Batch, BatchAdmin)


class SampleAdmin(admin.ModelAdmin):
    form = SampleAdminForm

admin.site.register(Sample, SampleAdmin)
