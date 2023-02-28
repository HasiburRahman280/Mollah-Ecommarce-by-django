from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    main_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_cat', blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name_plural = "Category"

class Product(models.Model): 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_product')
    mainimage = models.ImageField(upload_to='prouct_image')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    desc = models.TextField()
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name_plural = "Product"


class ProductRelatedImage(models.Model): 
    related_image = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_img')
    image = models.ImageField(upload_to='prouct_related_image/')