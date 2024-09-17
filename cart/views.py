from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from ecommerceapp.models import *
from django.http import JsonResponse
from django.contrib import messages

def cart_add(request, product_id):
    cart = Cart(request)

    # Get the product and quantity from the request
    size_id = request.POST.get('size', None)
    print(size_id)
    product = get_object_or_404(Product, id=product_id)
    product_qty = product_qty = int(request.POST.get('product_qty', 1))

    # Add product to cart
    added= cart.add(product=product, quantity=product_qty,size=size_id)
    cart_quantity = cart.__len__()
    if added :

        # Handle AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # This is an AJAX request
            response = JsonResponse({
                'qty': cart_quantity,
            })
            messages.success(request, "Product added to cart")
            return response

        # Handle normal form submission (non-AJAX request)
        else:
            messages.success(request, "Product added to cart")
            return redirect('dashboard')
    else:
        # Handle AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # This is an AJAX request
            response = JsonResponse({
                'qty': cart_quantity,
            })
            messages.warning(request, "Product already in cart")
            return response

        # Handle normal form submission (non-AJAX request)
        else:
            messages.warning(request, "Product already in cart")
            return redirect('dashboard')
    
def cart_summary(request):
    #get the cart
    cart=Cart(request)
    quantites=cart.get_quants
    cart_products=cart.get_prods
    totals=cart.cart_total()
    return render(request,'cart_summary.html',{
        'cart_products':cart_products,
        'quantities':quantites,
        'totals':totals
    })
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request,"Item removed from cart")
        return response
    
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size', None)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product_id=product_id, quantity=product_qty,size_id=size_id)
        # Assign the updated cart back to the session
        request.session['session_key'] = cart.cart
        response = JsonResponse({'qty': product_qty})
        messages.success(request,"Product updated successfully")
        return response