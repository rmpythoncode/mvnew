from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse
from vendor.models import Vendor
from products.models import Category, Product, SubCategory
# from django.db.models import Prefetch
from .models import Cart
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

# Create your views here.


def marketplace(request):
  vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:4]
  vendors_count = vendors.count()

  return render(request, 'marketplace/listings.html', {
    "vendors": vendors,
    "vendors_count": vendors_count,
  })



def search(request):
  
  print(request.GET)

  if not 'address' in request.GET:
    return redirect('marketplace')
  else:
    
      
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    #retorna lojas com os produtos procurados na keyword do search
    fetch_vendors_by_products = Product.objects.filter(product_name__icontains=keyword, is_available= True).values_list('vendor', flat=True)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_products) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    
    if latitude and longitude and radius:
      pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
    

      vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_products) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
        user_profile__location__distance_lte=(pnt, D(km=radius))
        ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
    
      for v in vendors:
        v.kms = round((v.distance.km)*1000)
    

    vendors_count = vendors.count()

    return render(request, 'marketplace/listings.html', {
      "vendors": vendors,
      "vendors_count": vendors_count,
      "source_location": address,
    })

def vendor_detail(request, vendor_slug):
  vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
  products = Product.objects.filter(vendor=vendor)
  categories = Category.objects.filter(vendor=vendor)
  categories_count = categories.count()


  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
  else:
    cart_items = None

  return render(request, 'marketplace/vendor_detail.html', {
    "vendor": vendor,
    "categories": categories,
    "categories_count": categories_count,
    "products": products,
    "cart_items": cart_items,
  })


def vendor_detail_by_category(request, vendor_slug, category_slug):
  
  vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)  
  category = get_object_or_404(Category, vendor=vendor, category_slug=category_slug)
  cat_dropdown = Category.objects.filter(vendor=vendor)
  produtcs = Product.objects.filter(vendor=vendor, category=category)

  subcat_dropdown = SubCategory.objects.filter(category=category)
  # for sub in subcat_dropdown:
  #   print(sub.category.slug)


  return render(request, 'marketplace/vendor_detail_by_category.html', {
    "vendor": vendor,
    "category": category,
    "cat_dropdown": cat_dropdown,
    "produtcs": produtcs,
    "subcat_dropdown": subcat_dropdown,
  })


def vendor_detail_by_subcategory(request, vendor_slug, category_slug, subcategory_slug):
  vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
  category = get_object_or_404(Category, vendor=vendor, category_slug=category_slug)
  subcategory = get_object_or_404(SubCategory, vendor=vendor, subcategory_slug=subcategory_slug)

  cat_dropdown = Category.objects.filter(vendor=vendor)
  subcat_dropdown = SubCategory.objects.filter(vendor=vendor, category=category)

  products = Product.objects.filter(vendor=vendor, category=category, subcategory=subcategory)
  for prod in products:
    print(prod.price)
    
  return render(request, 'marketplace/vendor_detail_by_subcategory.html', {
    "category": category,
    "subcategory": subcategory,
    "cat_dropdown": cat_dropdown,
    "subcat_dropdown": subcat_dropdown,
    "products": products,
    
  })

# def vendor_detail_by_subcategory(request, vendor_slug, subcategory_slug):
#   vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
#   subcategory = get_object_or_404(SubCategory, vendor=vendor, slug=subcategory_slug)
#   cat_dropdown = Category.objects.filter(vendor=vendor)
#   produtcs = Product.objects.filter(vendor=vendor, subcategory=subcategory)
#   subcategories_count = subcategory.count()
#   return render(request, 'marketplace/vendor_detail_by_subcategory.html', {
#     "vendor": vendor,
#     "subcategory": subcategory,
#     "cat_dropdown": cat_dropdown,
#     "produtcs": produtcs,
#     "subcategories_count": subcategories_count,
#   })






def ajax_increase_cart(request, prod_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      try:
        product = Product.objects.get(id=prod_id)
        try:
          chkCart = Cart.objects.get(user=request.user, product=product)
          chkCart.quantity += 1
          chkCart.save()
          return JsonResponse({'status': 'success', 'message': 'Uma unidade a mais do produto adicionado com sucesso.', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
        except:
          chkCart = Cart.objects.create(user=request.user, product=product, quantity=1)
          return JsonResponse({'status': 'success', 'message': 'Produto adicionado com sucesso.', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
      except:
        return JsonResponse({'status': 'failed', 'message': 'Este produto não existe.'})
    else:
      return JsonResponse({'status': 'failed', 'message': 'Solicitação Inválida.'})
  else:
    return JsonResponse({'status': 'login_required', 'message': 'Por favor entre para continuar.'})


def ajax_decrease_cart(request, prod_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      try:
        product = Product.objects.get(id=prod_id)
        try:
          chkCart = Cart.objects.get(user=request.user, product=product)
          if chkCart.quantity > 1:
            chkCart.quantity -= 1
            chkCart.save()
          else:
            chkCart.delete()
            chkCart.quantity = 0
          return JsonResponse({'status': 'success', 'message': 'Uma unidade a menos do produto subtraída com sucesso.', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
        except:
          return JsonResponse({'status': 'failed', 'message': 'Voce não tem este produto no carrinho.'})
      except:
        return JsonResponse({'status': 'failed', 'message': 'Este produto não existe.'})
    else:
      return JsonResponse({'status': 'failed', 'message': 'Solicitação Inválida.'})
  else:
    return JsonResponse({'status': 'login_required', 'message': 'Por favor entre para continuar.'})
  

@login_required(login_url='login')
def cart(request):
  return render(request, 'marketplace/cart.html')

def ajax_delete_cart(request, cart_id):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      try:
        #checa se tem o carrinho
        cart_item = Cart.objects.get(user=request.user, id=cart_id)
        if cart_item:
          cart_item.delete()
          return JsonResponse({'status': 'success', 'message': 'Produto excluído do carrinho.', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
      except:
        return JsonResponse({'status': 'failed', 'message': 'Produto não existe no carrinho'})
    else:
      return JsonResponse({'status': 'failed', 'message': 'Solicitação Inválida.'})


@login_required(login_url='login')
def cart_detail(request):
  cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
  cart_items_count = cart_items.count()
  

  return render(request, 'marketplace/cart_detail.html', {
    "cart_items_count": cart_items_count,
    "cart_items": cart_items,
  })