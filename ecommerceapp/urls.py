from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',views.dashboard,name='dashboard'),
    path('explore/',views.explore,name='explore'),
    path('product/<int:product_id>/', views.view_product, name='view_product'),
    path('category/<int:category_id>',views.single_category,name='category'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    
   
    
    path('login/',views.login_user,name='login_user'),
   path('logout/',views.logout_user,name='logout_user'),
   path('register/',views.register_user,name='register'),
   
   
   ####### Password reset by email
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    ### activate user email through email
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    
    ## order success
    path('order_success/',views.order_success,name="order_success"),
    
    ## register user address and verfying it 
    path('verify/',views.verify,name="verify"),
    
    
    ## display list of user orders
    
    path("orders/",views.orders,name="orders"),
    
    ### display the profile page
    
    path('profile/',views.profile, name="profile"),
    
    ## updating password
    
    path('update_password/',views.update_password,name='update_password'),
    path('update_info/',views.update_info,name='update_info'),

]