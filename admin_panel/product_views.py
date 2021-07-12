from django.shortcuts import render, redirect

def manage_product(request):
    return render(request, 'admin/products/all_product.html')

def add_product(request):
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        category = request.POST.get('category')
        slug = request.POST.get('slug')
        active = request.POST.get('active')
        return redirect('add_product')
    else:
        return redirect('add_product')
    return render(request, "admin/products/add-product.html")



def add_image(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        image = request.POST.get('image')
        category = request.POST.get('category')
        active = request.POST.get('active')
        return redirect('add_image')
    else:
        return redirect('add_image')
    return render(request, "admin/products/product-image.html")


def add_variation(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        title = request.POST.get('title')
        image = request.POST.get('image')
        category = request.POST.get('category')
        price = request.POST.get('price')
        active = request.POST.get('active')
        return redirect('add_variation')
    else:
        return redirect('add_variation')
    return render(request, "admin/product-variation.html")

    
def product_detail(request, id):
    return render(request, 'admin/product-detail.html')