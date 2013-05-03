from django import forms
from meadery.models import Product
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar


class WarehouseAdminForm(forms.ModelForm):
    class Meta:
        model = Warehouse


class RowAdminForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects)

    class Meta:
        model = Row


class ShelfAdminForm(forms.ModelForm):
    row = forms.ModelChoiceField(queryset=Row.objects)

    class Meta:
        model = Shelf


class BinAdminForm(forms.ModelForm):
    shelf = forms.ModelChoiceField(queryset=Shelf.objects)

    class Meta:
        model = Bin


class CrateAdminForm(forms.ModelForm):
    bin = forms.ModelChoiceField(queryset=Bin.objects)

    class Meta:
        model = Crate


# jars will likely be created en masse by the brewery!
class JarAdminForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.active)

    class Meta:
        model = Jar
