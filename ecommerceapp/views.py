from django.shortcuts import render
from .models import *

def dashboard(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    return render(request, 'index.html',{
        'categories': categories,
        'products':products
    })
