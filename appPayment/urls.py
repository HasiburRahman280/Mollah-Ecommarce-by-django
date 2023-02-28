from django.contrib import admin
from django.urls import path,include
from .  import views


urlpatterns = [
    path('checkout/',views.checkout, name='checkout'),
    path('complete/',views.complete, name='complete'),
    path('purchase/<tran_id>/<val_id>/',views.purchase, name='purchase')

]
