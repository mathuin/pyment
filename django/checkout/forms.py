from django import forms
from checkout.models import Order
import re


def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile(r'\D')
    return non_numbers.sub('', data)


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        # override default attributes
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id', )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Enter a valid phone number with area code.(e.g. 555-555-5555)')
        return self.cleaned_data['phone']
