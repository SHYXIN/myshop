import redis
from django.conf import settings
from .models import Product


# 连接redis

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB
                )

class Recommender(object):
    
    
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'
    
    def products_bought(self, products):
        product_ids=[p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # 获取从每个产品中购买的其他产品
                if product_id != with_id:
                    # 一起购买的产品的增量分数
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # 只有一个产品
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 
                                   0, -1, desc=True)[:max_results]
        else:
            # 生成一个临时key
            flat_ids = ''.join([str(i) for i in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # 多个产品，结合所有产品的得分
            # 将生成的排序集存储在一个临时键中
            keys = [self.get_product_key(i) for i in product_ids]
            # print(keys)
            # ['product:5:purchased_with', 'product:2:purchased_with']
            r.zunionstore(tmp_key, keys)
            # 删除已经在购物车的产品，推荐的是r.zrem（tmp_key，*product_ids）
            r.zrem(tmp_key, *product_ids)
            # 获得产品id的分数，后代排序
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # 删除临时key
            r.delete(tmp_key)
            
        suggested_products_ids = [int(i) for i in suggestions]
        # 获取建议的产品，并按【表现】顺序进行排序
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x:suggested_products_ids.index(x.id))
        return suggested_products
    
    def clear_purchases(self):
        for i in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(i))


