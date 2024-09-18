from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


## size model

class Size(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    name = models.CharField(max_length=3, choices=SIZE_CHOICES)

    def __str__(self):
        return self.get_name_display()

    

## Products models 
class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency=models.CharField(max_length=255,default="$")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0, max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name

class ClothingProduct(Product):
    sizes = models.ManyToManyField(Size, related_name='clothing_products', blank=True)
    
    def __str__(self):
        return f"{self.name} (Clothing)"
    
class ProductStock(models.Model):
    product = models.ForeignKey(Product, related_name='stock', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='stock', null=True, blank=True, on_delete=models.SET_NULL)  
    stock = models.PositiveIntegerField()
    
    def increaseStock():
        self.stock += 1
        self.save()
    def decreaseStock():
        if self.stock > 0:
            self.stock -= 1
            self.save()
    def is_in_stock(self):
        return self.stock > 0
    def __str__(self):
        return f"{self.product.name} ({self.size}) - {self.stock} units available"


## Order Item Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order {self.id} by {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
## Category model

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image=models.ImageField(upload_to='category_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name


## Customer model
class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)  # Format: MM/YY
    cvv = models.CharField(max_length=3, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
def create_profile(sender,instance,created,**kwargs):
    if created:
        # user_profile=Profile(user=instance)
        # user_profile.save()
        Profile.objects.create(user=instance)
#automate the profile thing
post_save.connect(create_profile,sender=User)

# Automatically create a Customer profile when a User is created
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    pass
    #instance.customer.save()