from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from cart.cart import Cart
def dashboard(request):
    categories=Category.objects.all()
    products = Product.objects.all().prefetch_related('stock__size')
    return render(request, 'index.html',{
        'categories': categories,
        'products':products
    })
    
    
def explore(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    return render(request, 'explore.html',{
        'categories': categories,
        'products':products
    })
    


def view_product(request, product_id):
    modify_mode = request.GET.get('modify', 'false') == 'true'
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantites = cart.get_quants()
    cart_items = quantites.get(str(product_id), {'quantity': 1, 'size': None})

    sizes = []
    selected_size = None
    if isinstance(product, ClothingProduct):
        sizes = product.sizes.all()  
        cart_items = cart.get_quants().get(str(product_id), {'quantity': 1, 'size': None})
        selected_size = cart_items['size']

    product_quantity = cart_items['quantity']
    categories = Category.objects.all()
    products = Product.objects.all()
    totals = cart.cart_total()
    print(sizes)
    context = {
        'singleproduct': product,
        'categories': categories,
        'products': products,
        'totals': totals,
        'modify': modify_mode,
        'sizes': sizes,
        'selected_size': selected_size,
        'product_quantity': product_quantity,
        'added': False
    }
    
    if modify_mode:
        context['added'] = True

    return render(request, 'single-product.html', context)


def single_category(request,category_id):
    category = get_object_or_404(Category, id=category_id)
    categories=Category.objects.all()
    products = Product.objects.filter(category=category).prefetch_related('stock__size')
    return render(request, 'single-category.html',{
        'singlecategory': category,
        'categories':categories,
        'products':products})
