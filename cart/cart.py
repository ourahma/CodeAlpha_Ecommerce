
from ecommerceapp.models import *
class Cart():
    def __init__(self,request):
        self.session=request.session
        
        #Get the current session key if it exists
        cart=self.session.get('session_key')
        
        #if the user is new no session, create one
        if 'session_key' not in request.session:
            cart = self.session['session_key']={}
        
        #make sure cart is available on all pages of site
        self.cart=cart
    def add(self, product, quantity=1, size=None):
        product_id = str(product.id)
        
        # Prepare cart entry for the product
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'size': None}
        else:
            return False
        # Update the quantity and size
        self.cart[product_id]['quantity'] += quantity
        if size:
            self.cart[product_id]['size'] = size # Store the size ID

        # Mark the session as modified to make sure it's saved
        print(self.cart)
        self.session.modified = True
        return True
        
    def __len__(self):
        return len(self.cart)
    
    
    def get_prods(self):
        #get ids from cart
        product_ids=self.cart.keys()
        #use ids to look up products in db
        products=Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantites=self.cart
        return quantites
    
    def update(self, product_id, quantity, size_id=None):
        product_id = str(product_id)

        # Check if the product is in the cart
        if product_id in self.cart:
            # Convert size_id to Size object if size_id is provided
            size = None
            if size_id:
                try:
                    size = Size.objects.get(id=size_id)
                except Size.DoesNotExist:
                    size = None
            
            # Update the quantity and size
            self.cart[product_id]['quantity'] = quantity
            if size:
                self.cart[product_id]['size'] = size.id
     
        self.session.modified = True
    
    def delete(self,product):
        product_id= str(product)
        #delete from dict
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified=True
    
    def cart_total(self):
        # Extract product IDs from the cart
        product_ids = self.cart.keys()

        # Fetch the products from the database
        products = Product.objects.filter(id__in=product_ids)

        total = 0
        for product_id, item in self.cart.items():
            product = products.get(id=product_id)
            quantity = item['quantity']
            if product.is_sale:
                total += product.sale_price * quantity
            else:
                total += product.price * quantity
        return total
    
    def clear(self):
        self.session.flush()