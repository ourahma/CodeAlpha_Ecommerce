from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from ecommerceapp.models import *
from django.http import JsonResponse
from django.contrib import messages
import stripe
from django.conf import settings

def cart_add(request, product_id):
    cart = Cart(request)

    # Get the product and quantity from the request
    size_id = request.POST.get('size_id', None)
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
        size_id = request.POST.get('size_id', None)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product_id=product_id, quantity=product_qty,size_id=size_id)
        # Assign the updated cart back to the session
        request.session['session_key'] = cart.cart
        response = JsonResponse({'qty': product_qty})
        messages.success(request,"Product updated successfully")
        return response
    
    
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login first to validate your order')
        return redirect('login')
    else:
        cart = Cart(request)

        # Handle POST request (confirming the order)
        if request.method == 'POST':
             # Retrieve payment information from the form
            card_number = request.POST.get('cardNumber')
            expiry_date = request.POST.get('expiryDate')
            cvv = request.POST.get('cvv')

            
            
            cart_items = cart.cart  # Accessing the raw cart data directly

            # Create a new order
            total_amount = cart.cart_total()
            order = Order.objects.create(
                customer=request.user.customer,
                total_amount=total_amount
            )

            # Process each item in the cart
            for product_id, item in cart_items.items():
                product = Product.objects.get(id=product_id)
                quantity = item['quantity']
                size = item['size'] if item['size'] else None

                # Check stock availability
                if size:
                    stock = ProductStock.objects.filter(product=product, size=size).first()
                    if not stock or stock.stock < quantity:
                        messgaes.error(request,'Problem in stock managing')
                        return redirect('cart_summary')  # Redirect to cart if stock issue
                
                # Create order item and update stock
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.sale_price if product.is_sale else product.price,
                    size=size
                )
                if size:
                    stock.stock -= quantity
                    stock.save()

            # Clear the cart after checkout
            cart.clear()
            return redirect('order_success')

        # Handle GET request (displaying the checkout page)
        else:
            products = cart.get_prods()  # Get products from the cart
            quantities = cart.get_quants()  # Get quantities and sizes from the cart
            total_amount = cart.cart_total()

            # Prepare the cart items to pass to the template
            cart_items = []
            for product in products:
                product_id = str(product.id)
                cart_items.append({
                    'product': product,
                    'quantity': quantities[product_id]['quantity'],
                    'size': quantities[product_id].get('size', None),
                })

            context = {
                'cart_items': cart_items,
                'total_amount': total_amount,
            }
            return render(request, 'checkout.html', context)
