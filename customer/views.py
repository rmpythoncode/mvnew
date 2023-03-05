from django.shortcuts import render

# Create your views here.

def c_dashboard(request):
  return render(request, 'customer/dashboard/dashboard.html')

def c_dashboard_orders(request):
  return render(request, 'customer/dashboard/orders.html')

def c_dashboard_order_view(request):
  return render(request, 'customer/dashboard/order_view.html')

def c_dashboard_products(request):
  return render(request, 'customer/dashboard/products.html')

def c_dashboard_product_edit(request):
  return render(request, 'customer/dashboard/product_edit.html')

def c_dashboard_customer_view(request):
  return render(request, 'customer/dashboard/customer_view.html')