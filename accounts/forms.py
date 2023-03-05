from django import forms
from .models import UserProfile, User
from .validators import allow_only_images_validator




class UserForm(forms.ModelForm):
  
  email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
  first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}))
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apelido'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmação da senha'}))


  
  class Meta:
    model = User
    
    fields = ('first_name', 'last_name', 'username', 'email', 'password')

  
  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    
    if password != confirm_password:
      raise forms.ValidationError(
        "Password não são iguais..."
      )


class UserProfileForm(forms.ModelForm):
  address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Pesquisar...', 'required': 'required'}))
  profile_picture = forms.FileField(widget=forms.FileInput(attrs={
    'class': 'btn btn-warning'}), validators=[allow_only_images_validator,])
  cover_photo = forms.FileField(widget=forms.FileInput(attrs={
    'class': 'btn btn-warning'}), validators=[allow_only_images_validator])

  # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
  # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
  
  class Meta:
    model = UserProfile
    fields = ['profile_picture', 'cover_photo', 'address', 'address_complement', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

  
  def __init__(self, *args, **kwargs):
    super(UserProfileForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      if field == 'latitude' or field == 'longitude':
        self.fields[field].widget.attrs['readonly'] = 'readonly'
    
    self.fields['cover_photo'].required = False
    self.fields['profile_picture'].required = False