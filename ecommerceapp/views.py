from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from cart.cart import Cart
from django.contrib.auth import *
from django.contrib import messages
from .forms import *
def dashboard(request):
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
            return redirect('validate')
        else:
            messages.ERROR(request,("There was an error, please try again "))
            return redirect('login')
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
            return redirect('home')
        else:
            # Afficher les erreurs de validation dans les messages d'erreur
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    
def validate(request):
    return render(request,'validate.html',{})