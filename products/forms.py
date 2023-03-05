from django import forms
from .models import SubCategory, Category, Product
from accounts.validators import allow_only_images_validator



class CategoryForm(forms.ModelForm):
  category_name = forms.CharField(widget=forms.TextInput(attrs={
  'style': 'font-size: 150%; font-weight: 530; background-color: lightgray;',
                }))
  description = forms.CharField(widget=forms.Textarea(attrs={
  'style': 'width: 100%; height: 150px; font-size: 150%; border-radius: 15px; border: none;'
  }))                                                              

  class Meta:
    model = Category
    fields = ['category_name', 'category_name', 'description']




class SubCategoryForm(forms.ModelForm):
  category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
   'style': 'margin-left:10px; height:40px; border-radius: 10px; border: none;'}))
 
  subcategory_name = forms.CharField(widget=forms.TextInput(attrs={
   'style': 'font-size: 150%; font-weight: 530; background-color: lightgray;',
  
                }))
  description = forms.CharField(widget=forms.Textarea(attrs={
  'style': 'width: 100%; height: 150px; font-size: 150%; border-radius: 15px; border: none;'
  }))                                                              

  class Meta:
    model = SubCategory
    fields = ['category', 'subcategory_name', 'description']



class ProductForm(forms.ModelForm):

  is_available = forms.BooleanField(widget=forms.CheckboxInput(attrs={
  	'checked': 'checked', 'style': 'width: 30px;'}))

  image = forms.FileField(widget=forms.FileInput(attrs={
    'class': 'btn btn-warning'}), validators=[allow_only_images_validator])
  
  product_name = forms.CharField(widget=forms.TextInput(attrs={
    'style': 'font-size: 150%; font-weight: 530; background-color: lightgray;'}))
  
  category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
    'style': 'margin-left:10px; height:40px; border-radius: 10px; border: none;'}))
  
  subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), widget=forms.Select(attrs={
   'style':'margin-left:10px; height:40px; border-radius: 10px; border: none;'}))

  description = forms.CharField(widget=forms.Textarea(attrs={
    'style': 'width: 100%; height: 150px; font-size: 150%; border-radius: 15px; border: none;'}))

  class Meta:
    model = Product
    fields = ['subcategory', 'category', 'product_name', 'description', 'price', 'sale_price', 'image', 'is_available']


  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['subcategory'].queryset = SubCategory.objects.all()


     
    # if 'category' in self.data:
    #   try:
    #     category_id = int(self.data.get('category'))
    #     self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
    #   except (ValueError, TypeError):
        
    #     pass
    # elif self.instance.pk:
    #   self.fields['subcategory'].queryset = self.instance.category.subcategory_set
  


