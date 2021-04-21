from django import forms
from django.core import validators


class CommentCreateForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "نام *", "class": "form-control"}),
        label="نام", required=True,
        validators=[validators.MaxLengthValidator(150, "نام و نام خانوادگی شما نمی تواند بیشتر از 150 کارکتر باشد")]
    )

    web_site = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "آدرس وب", "class": "form-control"}),
        label="آدرس وب", required=False,
        validators=[validators.MaxLengthValidator(200, "عنوان پیام شما نمی تواند بیشتر از 150 کارکتر باشد")]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "* ایمیل", "class": "form-control"}),
        label="ایمیل", required=True,
        validators=[validators.MaxLengthValidator(100, "ایمیل شما نمی تواند بیشتر از 100 کارکتر باشد")]
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "پیام *", "class": "form-control", "row": "8"}),
        label="پیام", required=True,
    )
