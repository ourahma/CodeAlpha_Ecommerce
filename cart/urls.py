from cart import views
from django.urls import path
urlpatterns = [
    path('',views.cart_summary,name='cart_summary'),
    path('add/<int:product_id>/', views.cart_add, name='add'),
    path('delete/',views.cart_delete,name='cart_delete'),
    path('update/',views.cart_update,name='cart_update'),
    #path('checkout/',views.checkout,name='checkout'),
    
    
    #### paying with paypal
    path('checkout/', views.payment_checkout, name='checkout_payment'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
<<<<<<< HEAD
    path('payment_failed', views.payment_failed, name='payment_failed'),
=======
    path('payment_failed', views.payment_failed, name='payment_failed')
    
    

>>>>>>> 9a7a0e255a2457621c4ad9a03d5356a66f9b2a78
]