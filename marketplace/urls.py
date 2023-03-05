from django.urls import path

from . import views

urlpatterns = [

    path('', views.marketplace, name='marketplace'),

    # Cart
    path('cart/', views.cart, name='cart'),

    # Order Detail
    path('cart_detail/', views.cart_detail, name='cart_detail'),

    # Order Detail
    path('search/', views.search, name='search'),




    # Increase/Decrease to Cart
    path('ajax_increase_cart/<int:prod_id>', views.ajax_increase_cart, name='ajax_increase_cart'),
    path('ajax_decrease_cart/<int:prod_id>', views.ajax_decrease_cart, name='ajax_decrease_cart'),

    # Delete item from Cart
    path('ajax_delete_cart/<int:cart_id>/', views.ajax_delete_cart, name='ajax_delete_cart'),


    
    path('<slug:vendor_slug>/<slug:category_slug>/<slug:subcategory_slug>/', views.vendor_detail_by_subcategory, name='vendor_detail_by_subcategory'),

    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    path('<slug:vendor_slug>/<slug:category_slug>/', views.vendor_detail_by_category, name='vendor_detail_by_category'),




 

    
    
   

]