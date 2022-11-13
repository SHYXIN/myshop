import redis
import time

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# r.zadd("zset1", n1=11, n2=22)
r.zadd("zset2", 'm1', 22, 'm2', 44)
print(r.zcard("zset1")) # 集合长度
print(r.zcard("zset2")) # 集合长度
print(r.zrange("zset1", 0, -1))   # 获取有序集合中所有元素
print(r.zrange("zset2", 0, -1, withscores=True))   # 获取有序集合中所有元素和分数