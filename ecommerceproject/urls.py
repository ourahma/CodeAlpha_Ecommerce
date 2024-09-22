from django.contrib import admin
from django.urls import path,include
from ecommerceapp import views
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ecommerceapp.urls')),
    path('cart/',include('cart.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)