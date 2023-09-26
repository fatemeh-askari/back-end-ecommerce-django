from django import forms
from django.core import validators
import re


def validate_no_persian(value):
    if re.search(r'[\u0600-\u06FF]', value):
        raise forms.ValidationError('کاراکترهای فارسی مجاز نیستند.')


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='لطفا آدرس ایمیل خود را وارد نمایید.',
        widget=forms.EmailInput(attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form', 'placeholder': ''}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='لطفا کلمه عبور خود را وارد نمایید.',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form', 'style': 'font-family: iransans'}),
        validators=[
            validators.MinLengthValidator(6, message='کلمه عبور باید حداقل 6 کاراکتر داشته باشد.'),
            validators.MaxLengthValidator(100),
            validate_no_persian,
        ]
    )
    confirm_password = forms.CharField(
        label='لطفا کلمه عبور خود را مجددا وارد نمایید.',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form', 'style': 'font-family: iransans'}),
        validators=[
            validators.MaxLengthValidator(100),
            validate_no_persian,
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password == confirm_password:
            return cleaned_data

        if password and password != confirm_password:
            self.add_error('confirm_password', 'کلمه عبور و تکرار کلمه عبور مغایرت دارند.')

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='لطفا آدرس ایمیل خود را وارد نمایید.',
        widget=forms.EmailInput(attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='لطفا کلمه عبور خود را وارد نمایید.',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form', 'style': 'font-family: iransans'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='لطفا آدرس ایمیل خود را وارد نمایید.',
        widget=forms.EmailInput(attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='لطفا کلمه عبور مورد نظر خود را وارد نمایید.',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form', 'style': 'font-family: iransans'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    );

    confirm_password = forms.CharField(
        label='لطفا کلمه عبور مورد نظر خود را مجددا وارد نمایید.',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs-5 mb-2 .text-dark border-form', 'style': 'font-family: iransans'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
