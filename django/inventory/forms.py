from django import forms
from meadery.models import Product
from inventory.models import Warehouse, Row, Shelf, Bin, Crate, Jar


class WarehouseAdminForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ["slug"]


class RowAdminForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects)

    class Meta:
        model = Row
        exclude = ["slug"]


class ShelfAdminForm(forms.ModelForm):
    row = forms.ModelChoiceField(queryset=Row.objects)

    class Meta:
        model = Shelf
        exclude = ["slug"]


class BinAdminForm(forms.ModelForm):
    shelf = forms.ModelChoiceField(queryset=Shelf.objects)

    class Meta:
        model = Bin
        exclude = ["slug"]


class CrateAdminForm(forms.ModelForm):
    bin = forms.ModelChoiceField(queryset=Bin.objects)

    class Meta:
        model = Crate
        exclude = ["slug"]


class JarAdminForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.active)

    class Meta:
        model = Jar
        exclude = ["slug"]
