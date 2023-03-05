from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .forms import VendorForm
from .models import Vendor
from products.models import Product, Category, SubCategory
from products.forms import CategoryForm, ProductForm, SubCategoryForm
from django.conf import settings
from django.template.defaultfilters import slugify

from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_profile(request):
  
  profile = get_object_or_404(UserProfile, user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)

  if request.method == "POST":
    profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    vendor_form = VendorForm(request.POST, instance=vendor)

    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      
      messages.success(request, 'Dados salvos com sucesso.')
      return redirect('v_profile')
    else:
      print(profile_form.errors)
      print(vendor_form.errors)

  profile_form = UserProfileForm(instance=profile)
  vendor_form = VendorForm(instance=vendor)

  return render(request, 'vendor/dashboard/v_profile.html', {
    'profile_form': profile_form,
    'vendor_form': vendor_form,
    'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_dashboard(request):
  return render(request, 'vendor/dashboard/dashboard.html',{
  })




def v_dashboard_orders(request):  
  return render(request, 'vendor/dashboard/orders.html')




def v_dashboard_order_view(request):
  return render(request, 'vendor/dashboard/order_view.html')




def categories(request):
  vendor = Vendor.objects.get(user=request.user)
  products = Product.objects.filter(vendor=vendor)
  
  categories = Category.objects.filter(vendor=vendor).prefetch_related(
    Prefetch(
    'subcatitems',
    queryset = SubCategory.objects.filter(vendor=vendor)
    )
  )
  categories_count = categories.count()
  products_count = products.count()
    
  return render(request, 'vendor/dashboard/categories.html', {
    'vendor': vendor,
    'categories': categories,
    'categories_count': categories_count,
    'products_count': products_count,
    'products': products,
  })


def subcategories(request):
  vendor = Vendor.objects.get(user=request.user)
  subcategories = SubCategory.objects.filter(vendor=vendor)
  subcategories_count = subcategories.count()

  return render(request, 'vendor/dashboard/subcategories.html', {
    'vendor': vendor,
    'subcategories': subcategories,
    'subcategories_count': subcategories_count,
  })



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def products_by_category(request, category_slug=None):
  vendor = Vendor.objects.get(user=request.user)
  category = get_object_or_404(Category, category_slug=category_slug)
  subcategories = SubCategory.objects.filter(vendor=vendor, category=category)
  subcategories_count = subcategories.count()
  products = Product.objects.filter(vendor=vendor, category=category)
  products_count = products.count()

  print(category)
  
  return render(request, 'vendor/dashboard/products_by_category.html', {
    'vendor': vendor,
    'category': category,
    'products': products,
    'products_count': products_count,
    "subcategories": subcategories,
    'subcategories_count': subcategories_count,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def products_by_subcategory(request, subcategory_slug=None):
  vendor = Vendor.objects.get(user=request.user)
  subcategory = get_object_or_404(SubCategory, subcategory_slug=subcategory_slug)
  products = Product.objects.filter(vendor=vendor, subcategory=subcategory)
  products_count = products.count()

  
  return render(request, 'vendor/dashboard/products_by_subcategory.html', {
    'vendor': vendor,
    'subcategory': subcategory,
    'products': products,
    'products_count': products_count,
  })



#####################
## CRUD categories ##
#####################

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
  vendor = Vendor.objects.get(user=request.user)

  if request.method == "POST":
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
      category_name = category_form.cleaned_data['category_name']
      category = category_form.save(commit=False)
      category.vendor = vendor
      
      category.save() #gera o id da categoria para colocar no category_slug
      category.category_slug = slugify(category_name)+'-'+str(category.id)
      category_form.save()
      messages.success(request, 'Dados gravados com sucesso.')      
      return HttpResponse('<script>history.go(-2);</script>')
      
    else:
      print(category_form.errors)
  else:
    category_form = CategoryForm()  

  return render(request, 'vendor/dashboard/add_category.html', {
    'category_form': category_form,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, category_slug=None):
  vendor = Vendor.objects.get(user=request.user)
  category = get_object_or_404(Category, category_slug=category_slug)

  if request.method == "POST":
    category_form = CategoryForm(request.POST, instance=category)
    if category_form.is_valid():
      category_name = category_form.cleaned_data['category_name']
      category = category_form.save(commit=False)
      category.vendor = vendor
      category.category_slug = slugify(category_name)
      category_form.save()
      messages.success(request, 'Dados gravados com sucesso.')
      return HttpResponse('<script>history.go(-2);</script>')
      
      # return redirect('categories')
    else:
      print(category_form.errors)
  else:
    category_form = CategoryForm(instance=category)  

  return render(request, 'vendor/dashboard/edit_category.html', {
    'category_form': category_form,
    'category': category,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
  category = get_object_or_404(Category, pk=pk)
  category.delete()
  messages.success(request, 'Categoria excluída com sucesso.')
  return redirect('categories')



########################
## CRUD subcategories ##
########################

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_subcategory(request):
  vendor = Vendor.objects.get(user=request.user)  
  

  if request.method == "POST":
    subcategory_form = SubCategoryForm(request.POST)
    if subcategory_form.is_valid():
      subcategory_name = subcategory_form.cleaned_data['subcategory_name']
      subcategory = subcategory_form.save(commit=False)
      subcategory.vendor = vendor
      subcategory.save() #gera o id da subcategoria para colocar no slug
      print("OK4")
      subcategory.subcategory_slug = slugify(subcategory_name)+'-'+str(subcategory.id)
      subcategory_form.save()
      messages.success(request, 'Dados gravados com sucesso.')
      return HttpResponse('<script>history.go(-2);</script>')
    else:
      print(subcategory_form.errors)
  else:
    subcategory_form = SubCategoryForm()  
    subcategory_form.fields['category'].queryset = Category.objects.filter(vendor=vendor)

  return render(request, 'vendor/dashboard/add_subcategory.html', {
    'subcategory_form': subcategory_form,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_subcategory(request, subcategory_slug):
  vendor = Vendor.objects.get(user=request.user)
  # category = get_object_or_404(Category, category_slug=category_slug)
  subcategory = get_object_or_404(SubCategory, subcategory_slug=subcategory_slug)
  
  if request.method == "POST":
    subcategory_form = SubCategoryForm(request.POST, instance=subcategory)
    if subcategory_form.is_valid():
      subcategory_name = subcategory_form.cleaned_data['subcategory_name']
      subcategory = subcategory_form.save(commit=False)
      subcategory.vendor = vendor
      subcategory.subcategory_slug = slugify(subcategory_name)
      subcategory_form.save()
      messages.success(request, 'Dados gravados com sucesso.')
      return HttpResponse('<script>history.go(-2);</script>')
    else:
      print(subcategory_form.errors)
  else:
    subcategory_form = SubCategoryForm(instance=subcategory)
  
  return render(request, 'vendor/dashboard/edit_subcategory.html', {
    'subcategory_form': subcategory_form,
    'subcategory': subcategory,
  })

def edit_category(request, category_slug=None):
  vendor = Vendor.objects.get(user=request.user)
  category = get_object_or_404(Category, category_slug=category_slug)

  if request.method == "POST":
    category_form = CategoryForm(request.POST, instance=category)
    if category_form.is_valid():
      category_name = category_form.cleaned_data['category_name']
      category = category_form.save(commit=False)
      category.vendor = vendor
      category.slug = slugify(category_name)
      category_form.save()
      messages.success(request, 'Dados gravados com sucesso.')
      return HttpResponse('<script>history.go(-2);</script>')
      
    else:
      print(category_form.errors)
  else:
    category_form = CategoryForm(instance=category)  

  return render(request, 'vendor/dashboard/edit_category.html', {
    'category_form': category_form,
    'category': category,
  })



def delete_subcategory(request):
  pass

# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def delete_category(request, pk=None):
#   category = get_object_or_404(Category, pk=pk)
#   category.delete()
#   messages.success(request, 'Categoria excluída com sucesso.')
#   return redirect('categories')
  





#####################
## CRUD Products ##
#####################


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def products(request):
  vendor = Vendor.objects.get(user=request.user)
  products = Product.objects.filter(vendor=vendor)
  products_count = products.count()

  return render(request, 'vendor/dashboard/products.html', {
    'products': products,
    'products_count': products_count,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product(request):
  vendor = Vendor.objects.get(user=request.user)
 

  if request.method == "POST":
    product_form = ProductForm(request.POST, request.FILES)
    if product_form.is_valid():
      product_name = product_form.cleaned_data['product_name']
      product = product_form.save(commit=False)
      product.vendor = vendor
      product.product_slug = slugify(product_name)
      product_form.save()
      messages.success(request, 'Dados gravados com sucesso.')
      return redirect('products_by_category', product.category.category_slug)
    else:
      print(product_form.errors)
  else:
    product_form = ProductForm()
    #modificar o formulário para somente aparecer as categorias
    #do vendedor logado filtra o product_form acima
    #inha abaixfica o queryset :-)
    product_form.fields['category'].queryset = Category.objects.filter(vendor=vendor)    
    

  return render(request, 'vendor/dashboard/add_product.html', {
    'product_form': product_form,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request, pk=None):
  vendor = Vendor.objects.get(user=request.user)
  product = get_object_or_404(Product, pk=pk)


  if request.method == "POST":
    product_form = ProductForm(request.POST, request.FILES, instance=product)
    if product_form.is_valid():
      product_name = product_form.cleaned_data['product_name']
      product = product_form.save(commit=False)
      product.vendor = vendor
      product.slug = slugify(product_name)
      product_form.save()
      messages.success(request, 'Dados gravados com sucesso.')
      return redirect('products')
    else:
      print(product_form.errors)
  else:
    product_form = ProductForm(instance=product) 
     

  return render(request, 'vendor/dashboard/edit_product.html', {
    'product_form': product_form,
    'product': product,
  })


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request, pk=None):
  product = get_object_or_404(Product, pk=pk)
  product.delete()
  messages.success(request, 'Produto excluído com sucesso.')
  return redirect('products')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def ajax_add_product_dropdown_subcategories(request):
  category_id = request.GET.get('category')
  subcategories = SubCategory.objects.filter(category_id=category_id)

  return render(request, 'products/ajax_add_product_dropdown_subcategories.html', {
    "subcategories": subcategories,
  })