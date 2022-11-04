from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart(object):
    
    def __init__(self, request):
        """
        初始化购物车
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 保存一个新的购物车在session中
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # 保存优惠券
        self.coupon_id = self.session.get('coupon_id')
    
    def add(self, product, quantity=1, override_quantity=False):
        """添加购物车或者更新数量"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price':str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        # 将会话标记为“已修改”，以确保它被保存
        self.session.modified = True
    
    def remove(self, product):
        """从购物车中删除"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """迭代购物车中的产品，并从数据库中获取产品。"""
        product_ids = self.cart.keys()
        # 获取产品对象，并将其添加到购物车中
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            # print(item)
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """购物车中项目的计数"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # 清空购物车
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100) * self.get_total_price())
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
        
