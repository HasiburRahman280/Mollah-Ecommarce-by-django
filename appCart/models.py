from django.db import models
from Store.models import Product
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart_user')
    cart_item = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_pro')
    quantity = models.IntegerField(default=1)
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_item.name

    def total_price(self):
        total = self.quantity * self.cart_item.price
        totals = format(total,'0.2f')
        return totals

    

class Order(models.Model):

    PAYMENT_CHOICE =(
        ('Cash On delivary','Cash On delivary'),
        ('SSLCommerze','SSLCommerze'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_user')
    order_item = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=50,blank=True,null=True)
    orderId = models.CharField(max_length=50,blank=True,null=True)
    payment_method =  models.CharField(max_length=50,choices=PAYMENT_CHOICE,default ='Cash On delivary',null=True)

    def order_item_total(self):
        total = 0
        for total_order_item in self.order_item.all():
            total +=float(total_order_item.total_price())
        return total






