from django.contrib import admin
from .models import Category, Product,ProductRelatedImage
# Register your models here.

class RelatedImageAdmin(admin.StackedInline):
    model = ProductRelatedImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [RelatedImageAdmin]
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category)
admin.site.register(Product,ProductAdmin)

