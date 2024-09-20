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
    products=Product.objects.all()
    return render(request, 'explore.html',{
        'categories': categories,
        'products':products
    })
    
def contact(request):
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
    quantites = cart.get_quants()
    cart_items = quantites.get(str(product_id), {'quantity': 1, 'size': None})

    if ClothingProduct.objects.filter(id=product_id).exists():
        
        clothing_product = ClothingProduct.objects.get(id=product_id)
        sizes = clothing_product.sizes.all()
        if sizes:  # Ensure sizes is not empty
           
            selected_size = cart.get_quants().get(str(product_id), {'quantity': 1, 'size': None})['size']
        else:
            sizes = []
            selected_size = None
    else:
        sizes = []
        selected_size = None

    product_quantity = cart_items['quantity']
    categories = Category.objects.all()
    products = Product.objects.all()
    totals = cart.cart_total()
    
    context = {
        'singleproduct': product,
        'categories': categories,
        'products': products,
        'totals': totals,
        'modify': modify_mode,
        'sizes': sizes,
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
            messages.ERROR(request,("There was an error, please try again "))
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
                })

            context = {
                'key':settings.STRIPE_PUBLIC_KEY,
                'cart_items': cart_items,
                'total_amount': total_amount,
            }
            return render(request,"verify.html",context)
        
    else:
        messages.error(request,"You must log in first")
        return redirect("login_user")