from ecommerceapp import views
from django.urls import path
urlpatterns = [

    path('',views.dashboard,name='dashboard'),
    path('explore/',views.explore,name='explore'),
    path('product/<int:product_id>/', views.view_product, name='view_product'),
    path('category/<int:category_id>',views.single_category,name='category'),
    
    path('validate/',views.validate,name='validate'),
    
    path('login/',views.login_user,name='login'),
   path('logout/',views.logout_user,name='logout'),
   path('register/',views.register_user,name='register'),
   

]