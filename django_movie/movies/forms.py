from django import forms
from .models import Reviews, Rating, RatingStars
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ReviewForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text', "captcha")


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStars.objects.all(
    ), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)
