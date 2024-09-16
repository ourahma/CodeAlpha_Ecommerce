from django.shortcuts import get_object_or_404
from .models import Product

def get_cart(request):
    cart = request.session.get('cart', {})
    return cart

def add_to_cart(request, product_id, quantity):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity
        }
    
    request.session['cart'] = cart

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    
    if product_id in cart:
        del cart[product_id]
    
    request.session['cart'] = cart

def update_cart(request, product_id, quantity):
    cart = get_cart(request)
    
    if product_id in cart:
        cart[product_id]['quantity'] = quantity
    
    request.session['cart'] = cart

def clear_cart(request):
    request.session['cart'] = {}
