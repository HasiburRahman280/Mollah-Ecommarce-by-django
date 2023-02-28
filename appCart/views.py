from django.shortcuts import render, get_object_or_404,redirect
from Store.models import Product
from .models import Cart
from .models import Order
from django.contrib import messages
# Create your views here.

def add_to_cart(request,slug):
    item = get_object_or_404(Product,slug=slug)
    if item:
        if(Cart.objects.filter(cart_item=item)):
            messages.success(request,'Product Has Been Already exists')
            return redirect('/')
        else:
            item_cart = Cart.objects.get_or_create(cart_item=item,user=request.user, purchase=False)
            quantity = request.POST.get('quantity')
            if quantity:
                item_cart[0].quantity = int(quantity)
                item_cart[0].save()
            item_order = Order.objects.filter(user=request.user,ordered=False)
            if item_order.exists():
                orders = item_order[0]
                if orders.order_item.filter(cart_item=item,user=request.user).exists():

                    quantity = request.POST.get('quantity')
                    print(quantity)
                    if quantity:
                        item_cart[0].quantity += quantity
                    else:
                        item_cart[0].quantity += 1
                    item_cart[0].save()
                    messages.success(request,'Product Has Been Successfully Added')
                    return redirect('/')
                    
                else:
                    orders.order_item.add(item_cart[0])
                    messages.success(request,'Product Has Been Successfully Added')
                    return redirect('/')

            else:
                orders = Order(user=request.user)
                orders.save()
                orders.order_item.add(item_cart[0])
                return redirect('/')


    


def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchase=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts':carts,
            'order':order,
        }
        return render(request,'store/cart_view.html',context)
    else:
        return redirect("/")


def remove_item(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(cart_item=item).exists():
            cart_item = Cart.objects.filter(cart_item=item,user=request.user,purchase=False)[0]
            order.order_item.remove(cart_item)
            cart_item.delete()
            return redirect('cart_view')

def increase_item(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(cart_item=item).exists():
            cart_item = Cart.objects.filter(cart_item=item,user=request.user,purchase=False)[0]
            if cart_item.quantity >= 1:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request,'Product Quantity Has Increased')
                return redirect('cart_view')

def decrease_item(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(cart_item=item).exists():
            cart_item = Cart.objects.filter(cart_item=item,user=request.user,purchase=False)[0]
            if cart_item.quantity >=1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request,'Product Quantity Has Increased')
                return redirect('cart_view')






    











