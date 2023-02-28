from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    #filter by category
    path('product-filter/<str:slug>',views.categorywiseproductfilter, name='cat_filter'),
    path('product-details/<str:c_slug>/<str:p_slug>/',views.product_details, name='product_details'),
    path('search-product/',views.search_product, name='search_product'),
    path('price-range/',views.price_range_filter, name='price_range_filter'),
]