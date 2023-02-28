from django.shortcuts import render
from .models import Product,Category,ProductRelatedImage
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    product_query = Product.objects.all()
    paginator = Paginator(product_query,6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products':products
    }
    return render(request,'index.html',context)

def categorywiseproductfilter(request,slug):
    if(Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug)
        context ={
            'products':products
        }
        return render(request,'product_filter.html',context)


def product_details(request,c_slug,p_slug):
    product_details = Product.objects.get(slug=p_slug)
    related_image = ProductRelatedImage.objects.filter(related_image=product_details)
    print(related_image)
    related_product =  Product.objects.filter(category=product_details.category).exclude(slug=p_slug)


    context ={
        'product_details':product_details,
        'related_image':related_image,
        'related_product':related_product,
    }
    return render(request,'store/product_details.html',context)

def search_product(request):
    if request.method == "GET":
        search_q = request.GET.get('search_item')
        if search_q:
            search_products = Product.objects.filter(name__icontains=search_q)
            return render(request,'store/search.html',{'search_products':search_products})
        else:
            return render(request,'store/search.html',{})

def price_range_filter(request):
    if request.method == "GET":
        minmum = request.GET.get('min_price')
        maximum = request.GET.get('max_price')
        products = Product.objects.filter(price__range=(minmum,maximum))
        print(products)
        return render(request,'store/price_filter.html',{'products':products})