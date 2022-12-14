from django import forms
from django.contrib.auth import get_user_model
from eshop.models import Product


class ProductReviewForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    score = forms.IntegerField(min_value=0, max_value=10)
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    text = forms.CharField(widget=forms.Textarea)
