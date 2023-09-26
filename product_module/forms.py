import re
from django import forms
from .models import ProductSupport

class ProductSupportForm(forms.ModelForm):
    class Meta:
        model = ProductSupport
        fields = ['full_name', 'email', 'title', 'message']
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'title': 'عنوان',
            'message': 'متن پیام',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control fs-5 mb-2 .text-dark', 'style': 'font-family: vazir-fa, Poppins, sans-serif'}),
            'email': forms.EmailInput(attrs={'class': 'form-control fs-5 mb-2 .text-dark',}),
            'title': forms.TextInput(attrs={'class': 'form-control fs-5 mb-2 .text-dark', 'style': 'font-family: vazir-fa'}),
            'message': forms.Textarea(attrs={'class': 'form-control fs-5 mb-2 .text-dark', 'rows': '5', 'id': 'message', 'style': 'font-family: vazir-fa'}),
        }
        error_messages = {
            'full_name': {
                'required': 'لطفاً نام و نام خانوادگی خود را وارد نمایید.',
            },
            'email': {
                'required': 'لطفاً ایمیل خود را وارد نمایید.',
            },
            'title': {
                'required': 'لطفاً موضوع پیام خود را وارد نمایید.',
            },
            'message': {
                'required': 'لطفاً متن پیام خود را وارد نمایید.',
            },
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[\u0600-\u06FF\sA-Za-z]+$', full_name):
            raise forms.ValidationError('نام و نام خانوادگی باید فقط شامل حروف باشد.')
        return full_name