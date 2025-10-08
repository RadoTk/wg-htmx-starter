from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "shopper_first_name",
            "shopper_name",       
            "shopper_email",
            "shopper_address",     
            "shopper_postal_code",
            "shopper_country",
        ]
        labels = {
            "shopper_first_name": "First name",
            "shopper_name": "Name",
            "shopper_email": "E-mail",
            "shopper_address": "Address",
            "shopper_postal_code": "Postal code",
            "shopper_country": "Country",
        }
        widgets = {
            "shopper_first_name": forms.TextInput(attrs={"placeholder": "Enter the given name for the purchaser"}),
            "shopper_name": forms.TextInput(attrs={"placeholder": "Enter the family name for the purchaser"}),
            "shopper_email": forms.EmailInput(attrs={"placeholder": "Provide an email"}),
            "shopper_address": forms.TextInput(attrs={"placeholder": "Street address or PO box"}),
            "shopper_postal_code": forms.TextInput(attrs={"placeholder": "Postal code"}),
            "shopper_country": forms.Select(),
        }

