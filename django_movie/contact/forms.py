from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import Contact


class ContactForm(forms.ModelForm):

    captch = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ("email", "captch")
        widgets = {"email": forms.TextInput(attrs={"class": "editContact"})}
