from django import forms
from django.core.exceptions import ValidationError
from .models import Ingredient, NewRecipe, NewBatch, Sample, NewProduct, ProductReview


class IngredientAdminForm(forms.ModelForm):
    class Meta:
        model = Ingredient

    def clean(self):
        cleaned_data = super(IngredientAdminForm, self).clean()
        cleaned_type = cleaned_data.get('type')
        cleaned_subtype = cleaned_data.get('subtype')
        cleaned_state = cleaned_data.get('state')
        if cleaned_type not in [type for (type, subtypes) in Ingredient.INGREDIENT_SUBTYPES if cleaned_subtype in [subtype for (subtype, name) in subtypes]]:
            raise ValidationError('Ingredient type and subtype must match.')
        if cleaned_state not in [state for (state, types) in Ingredient.STATE_TYPES if cleaned_type in types]:
            raise ValidationError('Ingredient state does not match type.')
        return cleaned_data


class NewRecipeAdminForm(forms.ModelForm):
    class Meta:
        model = NewRecipe

    # JMT: this is not yet working.
    # It's something to do with the fact that the related fields aren't yet saved.
    def clean(self):
        cleaned_data = super(NewRecipeAdminForm, self).clean()
        sugar_types = set([item.ingredient.subtype for item in self.instance.items(Ingredient.TYPE_SUGAR)])
        solvent_types = set([item.ingredient.subtype for item in self.instance.items(Ingredient.TYPE_SOLVENT)])
        solvent_temps = set([item.temp for item in self.instance.items(Ingredient.TYPE_SOLVENT)])
        flavor_types = set([item.ingredient.subtype for item in self.instance.items(Ingredient.TYPE_FLAVOR)])

        # Ingredient subtype checks.
        if len(sugar_types) == 0:
            raise ValidationError('At least one sugar source is required.')
        if Ingredient.SUGAR_HONEY not in sugar_types:
            raise ValidationError('At least one sugar source must be honey.')
        if not sugar_types.issubset(set(a for (a, b) in Ingredient.SUGAR_TYPES)):
            raise ValidationError('Unknown sugar type found -- check ingredients!')

        if len(solvent_types) == 0:
            raise ValidationError('At least one solvent source is required.')
        if len(solvent_temps) < 1:
            raise ValidationError('At least two solvents with different temperatures are required.')
        if not solvent_types.issubset(set(a for (a, b) in Ingredient.SOLVENT_TYPES)):
            raise ValidationError('Unknown solvent type found -- check ingredients!')

        if not flavor_types.issubset(set(a for (a, b) in Ingredient.FLAVOR_TYPES)):
            raise ValidationError('Unknown flavor type found -- check ingredients!')

        if len(self.instance.items(Ingredient.TYPE_YEAST)) == 0:
            raise ValidationError('At least one yeast is required.')

        cleaned_data['category'] = self.instance.suggested_category
        return cleaned_data


class NewBatchAdminForm(forms.ModelForm):
    class Meta:
        model = NewBatch


class SampleAdminForm(forms.ModelForm):
    class Meta:
        model = Sample


class NewProductAdminForm(forms.ModelForm):
    class Meta:
        model = NewProduct


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2',
                                                                'value': '1', 'class': 'quantity', 'maxlength': '5'}),
                                  error_messages={'invalid': 'Please enter a valid quantity.'},
                                  min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError('Cookies must be enabled.')
        return self.cleaned_data


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ('user', 'product', 'is_approved')
