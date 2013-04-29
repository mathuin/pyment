from django import forms
from .models import Honey, Water, Flavor, Yeast, Recipe, Batch, Sample


class HoneyAdminForm(forms.ModelForm):
    class Meta:
        model = Honey


class WaterAdminForm(forms.ModelForm):
    class Meta:
        model = Water


class FlavorAdminForm(forms.ModelForm):
    class Meta:
        model = Flavor


class YeastAdminForm(forms.ModelForm):
    class Meta:
        model = Yeast


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe


class BatchAdminForm(forms.ModelForm):
    class Meta:
        model = Batch


class SampleAdminForm(forms.ModelForm):
    class Meta:
        model = Honey

