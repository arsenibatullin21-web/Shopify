from django import forms
from .models import Product, Category, Size


class AddProductsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category',required=True)
    size = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), label='Sizes')
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'image', 'quantity', 'discount', 'rating', 'size', 'color', 'badges']
        widgets = {'name': forms.TextInput(attrs={'class': 'apx-form-input'}),
                   'price': forms.NumberInput(attrs={'class': 'apx-form-input'}),
                   'category': forms.Select(attrs={'class': 'apx-form-input'}),
                    'rating': forms.NumberInput(attrs={'class': 'apx-form-input'}),
                   'quantity': forms.NumberInput(attrs={'class': 'apx-form-input'}),
                   'size': forms.SelectMultiple(attrs={'class': 'apx-form-input'}),
                   'color': forms.SelectMultiple(attrs={'class': 'apx-form-input'}),
                   'image': forms.ClearableFileInput(attrs={'class': 'apx-form-input'}),
                   'description': forms.Textarea(attrs={'class': 'apx-form-textarea', 'rows': 6, 'placeholder': 'Write product description...'}),
                   'badges': forms.SelectMultiple(attrs={'class': 'apx-form-input'}),
                   'discount': forms.NumberInput(attrs={'class': 'apx-form-input'})

                   }
        labels = {
            'name': 'Product Name',
            'price': 'Price',
            'description': 'Description',
            'category': 'Category',
            'image': 'Image Url',
            'quantity': 'Stock Quantity',
            'discount': 'Discount',
            'rating': 'Rating',
            'size': 'Sizes',
            'color': 'Color',
            'badges': 'Badges'
        }