from django import forms
from .models import Review

class ProductFilterForm(forms.Form):
    product_search = forms.CharField(label="Product search", max_length=50, required=False)
    min_price = forms.DecimalField(label="Minimum price", decimal_places=2, required=False)
    max_price = forms.DecimalField(label="Maximum price", decimal_places=2, required=False)
    ave_rate = forms.DecimalField(label="Average rating", decimal_places=1, required=False)

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['stars','description']
