from django import forms
from .models import ShippingAdress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        exclude = ['user']