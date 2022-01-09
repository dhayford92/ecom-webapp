from datetime import timedelta
from django.shortcuts import render, redirect
from .models import*
from django.db.models import Q


def home(request):
    products = Product.objects.all()
    adproducts = Product.objects.all()
    context = {
        'products': products, 
        'adproducts': adproducts,
    }
    return render(request, 'store/index.html', context)



def ProductDetail(request, slug):
    product = Product.objects.get(slug=slug)
    related = Product.objects.filter(category__title__contains=product.category)
    context = {
        'product': product,
        'related': related,
    }
    return render(request, 'store/singleproduct.html', context)



def store(request):
    context = {
        'items': Product.objects.all().order_by('-id')
    }
    return render(request, 'store/product.html', context)



def category(request, title):
    products = Product.objects.filter(category__title__contains=title)
    context = {
        'products': products
    }
    return render(request, 'store/category.html', context)



def search(request):
    try:
        q = request.Get.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query': q, 'products': products}
        return render(request, 'store/search.html', context)
    else:
        context={}   
        return redirect('/')