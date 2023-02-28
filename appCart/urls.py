from django.contrib import admin
from django.urls import path
from appCart import views

urlpatterns = [
   path('cart/<str:slug>/',views.add_to_cart, name='add_to_cart'),
   path('cart_view/',views.cart_view, name='cart_view'),
   path('remove-item/<int:pk>/',views.remove_item, name='remove_item'),
   path('increase-item/<int:pk>/',views.increase_item, name='increase_item'),
   path('decrease-item/<int:pk>/',views.decrease_item, name='decrease_item'),
]
