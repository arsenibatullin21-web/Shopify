from django import forms

from main.models import Color, Size

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i  in range(1, 11)]

class CartProductAddForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=list(PRODUCT_QUANTITY_CHOICES),
        coerce=int,
        widget=forms.Select(attrs={'class': 'quantity-select'})
    )
    size = forms.ModelChoiceField(queryset=Size.objects.all(), required=True)
    color = forms.ModelChoiceField(queryset=Color.objects.all(), required=True)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)