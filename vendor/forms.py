from django import forms
from .models import Vendor


class VendorForm(forms.ModelForm):
  
  vendor_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome do Negócio',
        'style': 'font-size: 150%; font-weight: 530;'}))
  vendor_CNPJ = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CNPJ',
        'style': 'font-size: 150%; font-weight: 530;'}))

  class Meta:
    model = Vendor
    fields = ('vendor_name', 'vendor_CNPJ')


