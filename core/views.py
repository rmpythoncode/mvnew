from django.shortcuts import redirect, render
from django.contrib import messages
from vendor.models import Vendor
from core.settings import GOOGLE_API_KEY

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from products.models import Category, Product

def get_or_set_current_location(request):
  if 'lat' in request.session:
    lat = request.session['lat']
    lng = request.session['lng']
    return lng, lat
  elif 'lat' in request.GET:
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    request.session['lat']=lat
    request.session['lng']=lng
    return lng, lat
  else:
    return None



def home(request):
  if get_or_set_current_location(request) is not None:
    
    pnt = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))
    vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=1))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
    for v in vendors:
      v.kms = round((v.distance.km)*1000)
  else:    
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
  
  categories = Category.objects.all()
  products = Product.objects.filter(is_available=True)    
  return render(request, 'home.html', {
    "vendors": vendors,
    "GOOGLE_API_KEY": GOOGLE_API_KEY,
    "categories": categories,
    'products': products,
  })


