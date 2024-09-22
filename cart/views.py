from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from ecommerceapp.models import *
from django.http import JsonResponse
from django.contrib import messages
## for checkout
import paypalrestsdk
from django.conf import settings
from django.urls import reverse


<<<<<<< HEAD
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils import timezone 

=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78





def cart_add(request, product_id):
    cart = Cart(request)

    # Get the product and quantity from the request
    size_id = request.POST.get('size', None)
    print("size id ",size_id)
    product = get_object_or_404(Product, id=product_id)
    product_qty = product_qty = int(request.POST.get('product_qty', 1))

    # Add product to cart
    added= cart.add(product=product, quantity=product_qty,size=size_id)
    cart_quantity = cart.__len__()
    if added :

        # Handle AJAX request
<<<<<<< HEAD
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
=======
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # This is an AJAX request
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
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
<<<<<<< HEAD
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
=======
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # This is an AJAX request
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
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
        return redirect('login_user')
    else:
        cart = Cart(request)

        # Handle POST request (confirming the order)
        if request.method == 'POST':
            order = Order.objects.create(
                customer=user,
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
                'key':settings.STRIPE_PUBLIC_KEY,
                'cart_items': cart_items,
                'total_amount': total_amount,
            }
            return render(request, 'verify.html', context)




#### paypal checkout section

paypalrestsdk.configure({
    "mode": "sandbox",  
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def create_payment(request):
    if request.method == 'POST':
        user=request.user
        cart=Cart(request)
<<<<<<< HEAD
        products = cart.get_prods()  
        quantities = cart.get_quants()  
=======
        products = cart.get_prods()  # Get products from the cart
        quantities = cart.get_quants()  # Get quantities and sizes from the cart
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
        total_amount = cart.cart_total()
        order = Order.objects.create(
                customer=user.customer,
                total_amount=total_amount
            )
        cart_items = cart.get_quants()
            # Process each item in the cart
        for product_id, item in cart_items.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            size = item['size'] if item['size'] else None

                # Check stock availability
            if size:
                stock = ProductStock.objects.filter(product=product, size=size).first()
                if not stock or stock.stock < quantity:
                    messages.error(request,'Problem in stock managing')
                    return redirect('cart_summary')  # Redirect to cart if stock issue
                size_object=Size.objects.get(id=size)
                # Create order item and update stock
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.sale_price if product.is_sale else product.price,
                    size=size_object
                )
                if size:
                    stock.stock -= quantity
                    stock.save()
            else:
                stock = ProductStock.objects.filter(product=product).first()
                if not stock or stock.stock < quantity:
                    messages.error(request, 'Problem in stock management')
                    return redirect('cart_summary')
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.sale_price if product.is_sale else product.price,
                    size=None  
                )
                
                
                stock.decreaseStock(quantity)
<<<<<<< HEAD
                
                send_validate_order_email(request.user,order,total_amount,timezone.now())
=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('execute_payment')),
                "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
            },
            "transactions": [
                {
                    "amount": {
                        "total": str(total_amount), 
                        "currency": "USD",
                    },
                    "description": "Payment for Product/Service",
                }
            ],
        })
    

        if payment.create():
            return redirect(payment.links[1].href)  # Redirect to PayPal for payment
        else:
            return render(request, 'payment_failed.html')
    else:
        messages.error(request,"Access denied ")
        return redirect("dashboard")

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        cart = Cart(request)
        cart.clear()
<<<<<<< HEAD
        
=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

def payment_checkout(request):
<<<<<<< HEAD
    user = request.user
    return render(request, 'checkout.html',{})

def payment_failed(request):
    return render(request, 'payment_failed.html')


def send_validate_order_email(user,order,total_amount,order_date):
    # Send email to user to validate order
    email_subject = 'Your Order is Confirmed!'
    email_body = render_to_string('order_confirmation_email.html', {
        'user': user,
        'order': order,
        'total_amount':total_amount,
        'order_date':order_date
    })

    
    send_mail(
        subject=email_subject,
        message=email_body,  
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False, 
        html_message=email_body  
    )
=======
    return render(request, 'checkout.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
