from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BillingAddressForm,PaymentMethodForm
from .models import BillingAddress
from appCart.models import Order,Cart
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

#payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
# Create your views here.

def checkout(request):
    save_address = BillingAddress.objects.get_or_create(user=request.user)
    save_address = save_address[0]
    form = BillingAddressForm(instance=save_address)

    order_qs = Order.objects.filter(user=request.user,ordered=False)[0]
    order_item = order_qs.order_item.all()
    order_item_count = order_qs.order_item.count()
    # print(order_item_count)
    order_totals = order_qs.order_item_total()

    if request.method =='post' or request.method =='POST':
        form = BillingAddressForm(request.POST,instance=save_address)
        pay_form = PaymentMethodForm(request.POST,instance=order_qs)

        if not save_address.is_fully_filled():
            return redirect('checkout')

        if form.is_valid() and pay_form.is_valid():
            form.save()
            payment = pay_form.save(commit=False)
            if payment.payment_method == "Cash On delivary":
                order_qs = Order.objects.filter(user=request.user,ordered=False)
                print(order_qs)
                orders = order_qs[0]
                print(order_qs)
                orders.ordered = True
                orders.paymentId = payment.payment_method
                orders.orderId = get_random_string(10)
                orders.save()
                cart_items = Cart.objects.filter(user=request.user,purchase=False)
                print(cart_items)
                for item in cart_items:
                    item.purchase = True
                    item.save()
                return redirect('/')

            if payment.payment_method == "SSLCommerze":
                payment.save()
                store_id = 'abc626e225657a3c'
                API_key = 'abc626e225657a3c@ssl'

                mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

                status_url = request.build_absolute_uri(reverse('complete'))
                print(status_url)

                mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

                mypayment.set_product_integration(total_amount=Decimal(order_totals), currency='BDT', product_category='Mixed', product_name=order_item, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')

                current_user =  request.user

                mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.profile.email, address1=current_user.profile.address, address2=current_user.profile.address, city=current_user.profile.gender, postcode='66', country='Bangladesh', phone=current_user.profile.phone)

                mypayment.set_shipping_info(shipping_to=save_address.first_name, address=save_address.address, city=save_address.city, postcode='66', country='Bangladesh')

                response_data = mypayment.init_payment()

                return redirect(response_data['GatewayPageURL'])

    pay_form = PaymentMethodForm()
    context ={
        'form':form,
        'pay_form':pay_form,
        'order_item':order_item,
        'order_totals':order_totals,

        
    }
    return render(request, 'payment/checkout.html',context)
    
@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':

        status = request.POST['status']

        if status == 'VALID':
            tran_id = request.POST['tran_id']
            val_id = request.POST['val_id']
            messages.success(request,f"Payment Is Successfully!")
            return HttpResponseRedirect(reverse(purchase,kwargs={'tran_id':tran_id,'val_id':val_id}))
        
        elif status == 'FAILED':
            messages.warning(request,f"Payment Failed ! Please Try Again After! 5 second Home Page will be redirected")
            return redirect('complete')
        elif status == 'CANCEL':
            messages.warning(request,f"Payment Cancel ! After 5 second Home Page will be redirected")
            return redirect('complete')
    return render(request, 'payment/complete.html')


def purchase(request,tran_id,val_id):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    orders = order_qs[0]
    orders.ordered = True
    orders.paymentId = tran_id
    orders.orderId = val_id
    orders.save()
    cart_items = Cart.objects.filter(user=request.user,purchase=False)
    for item in cart_items:
        item.purchase = True
        item.save()
    return redirect('complete')