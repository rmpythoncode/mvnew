from django.urls import path
from . import views




urlpatterns = [
    
    path('v_dashboard/', views.v_dashboard, name='v_dashboard'),
    path('v_dashboard_orders/', views.v_dashboard_orders, name='v_dashboard_orders'),
    path('v_dashboard_order_view/', views.v_dashboard_order_view, name='v_dashboard_order_view'),

    path('v_dashboard/categories/', views.categories, name='categories'),

    path('v_dashboard/products/', views.products, name='products'),
    
    path('products_by_category/<str:category_slug>/', views.products_by_category, name='products_by_category'),
    path('products_by_subcategory/<str:subcategory_slug>/', views.products_by_subcategory, name='products_by_subcategory'),
    path('v_dashboard/v_profile/', views.v_profile, name='v_profile'),


    # Category CRUD
    path('v_dashboard/category/add/', views.add_category, name='add_category'),
    path('v_dashboard/category/edit/<str:category_slug>/', views.edit_category, name='edit_category'),
    path('v_dashboard/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # SubCategory CRUD
    path('v_dashboard/subcategories/', views.subcategories, name='subcategories'),
    path('v_dashboard/subcategory/add/', views.add_subcategory, name='add_subcategory'),
    path('v_dashboard/subcategory/edit/<str:subcategory_slug>/', views.edit_subcategory, name='edit_subcategory'),
    path('v_dashboard/subcategory/delete/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
    
    # Product CRUD
    path('v_dashboard/product/add/', views.add_product, name='add_product'),
    path('v_dashboard/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('v_dashboard/product/delete/<int:pk>/', views.delete_product, name='delete_product'),

    path('ajax/ajax_add_product_dropdown_subcategories/', views.ajax_add_product_dropdown_subcategories, name='ajax_add_product_dropdown_subcategories'),
 
    
]
