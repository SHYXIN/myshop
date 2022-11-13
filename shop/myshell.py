
# 获取商品
from shop.models import Product
black_tea = Product.objects.get(translations__name='Black tea')
red_tea = Product.objects.get(translations__name='Red tea')
green_tea = Product.objects.get(translations__name='Green tea')
tea_powder = Product.objects.get(translations__name='Tea powder')

# 产生购买测试数据
from shop.recommender import Recommender
r = Recommender()
r.products_bought([black_tea, red_tea])
r.products_bought([black_tea, green_tea])
r.products_bought([red_tea, black_tea, tea_powder])
r.products_bought([green_tea, tea_powder])
r.products_bought([black_tea, tea_powder])
r.products_bought([red_tea, green_tea])

# 产生推荐内容
from django.utils.translation import activate
activate('en')

# 购买单个产品,产生的推荐
r.suggest_products_for([black_tea])
r.suggest_products_for([red_tea])
r.suggest_products_for([green_tea])
r.suggest_products_for([tea_powder])

# 购买多个产品，根据积分值产生的推荐

r.suggest_products_for([black_tea, red_tea])
r.suggest_products_for([green_tea, red_tea])
r.suggest_products_for([tea_powder, black_tea])