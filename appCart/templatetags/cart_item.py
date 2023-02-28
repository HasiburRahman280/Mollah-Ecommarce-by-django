from django import template
from appCart.models import Cart,Order

register = template.Library()

@register.filter
def cart_items(user):
    total_cart_item = Cart.objects.filter(user=user,purchase=False)
    return total_cart_item

@register.filter
def total_order_price(user):
    total_order_item_price = Order.objects.filter(user=user,ordered=False)
    if total_order_item_price.exists():
        return total_order_item_price[0].order_item_total()
    else:
        return 0

@register.filter
def total_cart_item_count(user):
    cart_item_count = Cart.objects.filter(user=user,purchase=False)
    return cart_item_count.count()