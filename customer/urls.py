from django.urls import path

from . import views

urlpatterns = [
    
    path('c_dashboard/', views.c_dashboard, name='c_dashboard'),

    path('c_dashboard_orders/', views.c_dashboard_orders, name='c_dashbord_orders'),

    path('c_dashboard_order_view/', views.c_dashboard_order_view, name='c_dashboard_order_view'),

    path('c_dashboard_products/', views.c_dashboard_products, name='c_dashboard_products'),

    path('c_dashboard_product_edit/', views.c_dashboard_product_edit, name='c_dashboard_product_edit'),

    path('c_dashboard_customer_view/', views.c_dashboard_customer_view, name='c_dashboard_customer_view'),
    
]

