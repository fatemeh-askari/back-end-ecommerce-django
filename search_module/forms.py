from django import forms


class ProductSearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'جستجو در مقالات و محصولات',
                'class': 'form-control',  # Add your custom classes here
                'style': 'max-width: 50rem; font-size: 1.25rem; font-family: iransans',  # Add your custom styles here
            }
        ),
    )
