
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
    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)
        self.session.modified=True
        
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
    
    def update(self,product_id,quantity):
        product_id=str(product_id)
        product_qty=int(quantity)
        ##get the cart
        
        ourcart=self.cart
        #uodate dict
        ourcart[product_id]=product_qty
        
        self.session.modified = True
        
        thing=self.cart
        return thing
    
    def delete(self,product):
        product_id= str(product)
        #delete from dict
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified=True
    
    def cart_total(self):
        #get product ids
        product_ids=self.cart.keys()
        #lookip the keyys in the db
        products=Product.objects.filter(id__in=product_ids)
        #get quantities
        quantites=self.cart
        
        total=0
        for key,value in quantites.items():
            key=int(key)
            for product in products:
                if product.id==key:
                    if product.is_sale:
                        total=total+(product.sale_price*value)
                    else:
                        total=total+(product.price*value)
        return total