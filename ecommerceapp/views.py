from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from cart.cart import Cart
from django.contrib.auth import *
from django.contrib import messages
from .forms import *
# views to reset password
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.forms import *

from django.template.loader import render_to_string
from django.core.mail import send_mail

<<<<<<< HEAD
from django.conf import settings
=======

>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78


def dashboard(request):
    cart=Cart(request)
    print(cart.get_quants())
    
    categories=Category.objects.all()
    products = Product.objects.all().prefetch_related('stock__size')
    for product in products:
        # Sum the stock for all sizes of this product
        product.in_stock = sum(stock.stock for stock in product.stock.all()) > 0
        
    return render(request, 'index.html',{
        'categories': categories,
        'products':products
    })
    
    
def explore(request):
    categories=Category.objects.all()
<<<<<<< HEAD
    products = Product.objects.all().prefetch_related('stock__size')
    for product in products:
        
        product.in_stock = sum(stock.stock for stock in product.stock.all()) > 0
=======
    products=Product.objects.all()
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
    return render(request, 'explore.html',{
        'categories': categories,
        'products':products
    })
    
def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save the notification
        admin = User.objects.get(is_staff=True)
        
        subject = "Contact admin form :  "+ email
        email_message = render_to_string('notification_email.html', {
                'user': admin,
                'message': message
            })
        send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [admin.email])

        messages.success(request,"Your message is sent seccessfully! ")
        return redirect('contact')  
    else:
        categories=Category.objects.all()
        products=Product.objects.all()
        return render(request, 'contact.html',{
            'categories': categories,
            'products':products
        })
    
    
def about(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    return render(request, 'about.html',{
        'categories': categories,
        'products':products
    })

def view_product(request, product_id):
    modify_mode = request.GET.get('modify', 'false') == 'true'
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    total_stock = sum(stock.stock for stock in product.stock.all())
    is_in_stock = total_stock > 0
    quantities = cart.get_quants()
    cart_items = quantities.get(str(product_id), {'quantity': 1, 'size': None})
    
    sizes_in_stock = []
    selected_size = None
    
    if ClothingProduct.objects.filter(id=product_id).exists():
        clothing_product = ClothingProduct.objects.get(id=product_id)
        
        # Get all sizes available in stock
        available_stocks = ProductStock.objects.filter(product=clothing_product, stock__gt=0)
        sizes_in_stock = [stock.size for stock in available_stocks if stock.size]  # List of sizes with stock
        
        # Get the selected size from the cart
        selected_size = cart.get_quants().get(str(product_id), {'quantity': 1, 'size': None})['size']
        if selected_size:
            selected_size = Size.objects.get(id=selected_size)  # Fetch the selected size object
            
    product_quantity = cart_items['quantity']
    categories = Category.objects.all()
    products = Product.objects.all()
    totals = cart.cart_total()
    
    context = {
        'singleproduct': product,
        'categories': categories,
        'products': products,
        'totals': totals,
<<<<<<< HEAD
        'total_stock':total_stock,
=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
        'modify': modify_mode,
        'sizes': sizes_in_stock,  # Pass sizes that are in stock
        'selected_size': selected_size,
        'product_quantity': product_quantity,
        'added': False,
        'is_in_stock': is_in_stock
    }
    
    if modify_mode:
        context['added'] = True

    return render(request, 'single-product.html', context)



def single_category(request,category_id):
    category = get_object_or_404(Category, id=category_id)
    categories=Category.objects.all()
    products = Product.objects.filter(category=category).prefetch_related('stock__size')
    for product in products:
        # Sum the stock for all sizes of this product
        product.in_stock = sum(stock.stock for stock in product.stock.all()) > 0
    return render(request, 'single-category.html',{
        'singlecategory': category,
        'categories':categories,
        'products':products})


def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in "))
            return redirect('verify')
        else:
<<<<<<< HEAD
            messages.error(request,"There was an error, please try again ")
=======
            messages.ERROR(request,("There was an error, please try again "))
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
            return redirect('login_user')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been log out"))
    return redirect('dashboard')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully")
            return redirect('dashboard')
        else:
            # Afficher les erreurs de validation dans les messages d'erreur
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    
def order_success(request):
    return render(request,'order_success.html',{})


############################## RESERT PASSWORD BY EMAIL

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'forget_password_from_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        users = list(self.get_users(email))
        
        if not users:
           
            messages.error(self.request, "No user registered with this email!!")
            return redirect("login_user")
       
        return super().form_valid(form)

    def form_invalid(self, form):
        
        print("form is unvalid")
        return redirect("login_user")

    def get_users(self, email):
        UserModel = get_user_model()
        active_users = UserModel._default_manager.filter(
            email__iexact=email,
            is_active=True,
        )
        return (u for u in active_users if u.has_usable_password())
    


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        messages.success(request, 'Vous avez activé votre compte. Vous pouvez maintenant vous connecter.')
        return redirect('login_user')
    else:
        messages.error(request, 'Le lien d\'activation est invalide !')
        return redirect('register')
    
    
def verify(request):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            address=request.POST.get("address")
            city=request.POST.get("city")
            country=request.POST.get("country")
            postal_code=request.POST.get("postal_code")
            user=request.user
            user.address=address
            user.city=city
            user.country=country
            user.postal_code=postal_code
            user.save()
            return redirect("checkout_payment")
        else:
            user=request.user
            print(user)
            cart=Cart(request)
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
                    'user':user,
                })

            context = {
<<<<<<< HEAD
                
=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
                'key':settings.STRIPE_PUBLIC_KEY,
                'cart_items': cart_items,
                'total_amount': total_amount,
            }
            return render(request,"verify.html",context)
        
    else:
        messages.error(request,"You must log in first")
        return redirect("login_user")
    
    
def orders(request):
    user = request.user
    orders = Order.objects.filter(customer=user.customer).prefetch_related('items')
    return render(request, 'user_orders.html', {'orders': orders})

def profile(request):
    user=request.user
    updatepswdform=ChangePasswordForm(request.user,request.POST)
    updateuserform=UpdateUserForm(user=request.user)
<<<<<<< HEAD
    infouserform=UserInfoForm(user=request.user)
=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
    
    
    return render(request,'profile.html',{
        'user':user,
        'updatepswdform':updatepswdform,
        'updateuserform':updateuserform,
<<<<<<< HEAD
        'infouserform':infouserform
=======
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
        })
    
    
    
    
def update_password(request):
    
    if request.user.is_authenticated:
        current_user=request.user
        if request.method =='POST':
            form=ChangePasswordForm(current_user,request.POST)
            
            # if the form valid
            
            if form.is_valid():
                form.save()
                messages.success(request,"Your password has been up to date ")
                login(request,current_user)
                return redirect('profile')
            else:
                for error in form.errors.items():
                    messages.error(request,error)
                    return redirect('profile')
        else:
            form=ChangePasswordForm(current_user)
            return render(request,'profile.html',{
                'form':form
            })
    else:
        messages.error(request,"You must be logged in ")
        return redirect('dashboard')
    
    
def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Customer.objects.get(user=request.user)
<<<<<<< HEAD
            form = UpdateUserForm(request.POST or None, instance=current_user)
        except Customer.DoesNotExist:
            # Handle the case where Profile does not exist for the user
            messages.error(request, "Customer does not exist. Please create your profile.")
            return redirect('profile')  # Redirect to a view to create the profile
        
        if  form.is_valid():
            print(True)
            form.save()
            messages.success(request, "Your info has been updated")
            return redirect('profile')
        else:
            messages.error(request,form.error)
            return redirect("profile")
        
        return render(request, "profile.html", {'form': form})
    else:
        messages.error(request, "You must be logged in")
        return redirect('dashboard')
    
def update_address_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Customer.objects.get(user=request.user)
            form = UserInfoForm(request.POST or None, instance=current_user)
        except Customer.DoesNotExist:
            # Handle the case where Profile does not exist for the user
            messages.error(request, "Customer does not exist. Please create your profile.")
            return redirect('home')  # Redirect to a view to create the profile
=======
            form = UserInfoForm(request.POST or None, instance=current_user)
        except Customer.DoesNotExist:
            # Handle the case where Profile does not exist for the user
            messages.error(request, "Profile does not exist. Please create your profile.")
            return redirect('profile')  # Redirect to a view to create the profile
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated")
            return redirect('profile')
        else:
            messages.error(request,form.error)
            return redirect("profile")
        
        return render(request, "profile.html", {'form': form})
    else:
        messages.error(request, "You must be logged in")
<<<<<<< HEAD
        return redirect('profile')
=======
        return redirect('dashboard')
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
