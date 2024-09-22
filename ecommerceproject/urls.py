from django.contrib import admin
from django.urls import path,include
from ecommerceapp import views
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ecommerceapp.urls')),
<<<<<<< HEAD
    path('cart/',include('cart.urls')),
=======
    path('cart',include('cart.urls')),
>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)