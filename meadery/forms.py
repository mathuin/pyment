from django import forms
from .models import Honey, Water, Flavor, Yeast, Recipe, Batch, Sample, Product, ProductReview


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
        model = Sample


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product


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
