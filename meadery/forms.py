from django import forms
from django.core.exceptions import ValidationError
from .models import Ingredient, Recipe, Batch, Sample, Product, ProductReview


class IngredientAdminForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['slug']

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


class IngredientItemFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        items = {}
        for form in self.forms:
            try:
                if form.cleaned_data:
                    form_item = {'ingredient': form.cleaned_data.get('ingredient'),
                                 'amount': form.cleaned_data.get('amount'),
                                 'temp': form.cleaned_data.get('temp')}
                    items.append(form_item)
            except AttributeError:
                pass
        sugar_types = set([item['ingredient'].subtype for item in items if item['ingredient'].type == Ingredient.TYPE_SUGAR])
        solvent_types = set([item['ingredient'].subtype for item in items if item['ingredient'].type == Ingredient.TYPE_SOLVENT])
        solvent_temps = set([item['temp'] for item in items if item['ingredient'].type == Ingredient.TYPE_SOLVENT])
        flavor_types = set([item['ingredient'].subtype for item in items if item['ingredient'].type == Ingredient.TYPE_FLAVOR])
        yeast_types = set([item['ingredient'].subtype for item in items if item['ingredient'].type == Ingredient.TYPE_YEAST])

        # Ingredient subtype checks.
        if len(sugar_types) == 0:
            raise ValidationError('At least one sugar source is required.')
        if Ingredient.SUGAR_HONEY not in sugar_types:
            raise ValidationError('At least one sugar source must be honey.')
        if not sugar_types.issubset(set(a for (a, b) in Ingredient.SUGAR_TYPES)):
            raise ValidationError('Unknown sugar type found -- check ingredients!')

        if len(solvent_temps) < 2:
            raise ValidationError('At least two solvents with different temperatures are required.')
        if not solvent_types.issubset(set(a for (a, b) in Ingredient.SOLVENT_TYPES)):
            raise ValidationError('Unknown solvent type found -- check ingredients!')

        if not flavor_types.issubset(set(a for (a, b) in Ingredient.FLAVOR_TYPES)):
            raise ValidationError('Unknown flavor type found -- check ingredients!')

        if len(yeast_types) == 0:
            raise ValidationError('At least one yeast is required.')

        if not yeast_types.issubset(set(a for (a, b) in Ingredient.YEAST_TYPES)):
            raise ValidationError('Unknown yeast type found -- check ingredients!')

        # Now that we know the mead is valid, set the category.
        self.instance.category = self.instance.suggested_category(sugar_types, solvent_types, flavor_types)


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['slug']


class BatchAdminForm(forms.ModelForm):
    class Meta:
        model = Batch
        exclude = ['slug']


class SampleAdminForm(forms.ModelForm):
    class Meta:
        model = Sample
        exclude = ['slug']


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug']


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
