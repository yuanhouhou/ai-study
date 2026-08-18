import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


#创建Redis 的连接对象

redis_client = redis.Redis(
    host=REDIS_HOST,  # Redis 服务器的主机名或 IP 地址
    port=REDIS_PORT,  # Redis 服务端口
    db=REDIS_DB,  # Redis 数据库编号：0-15
    decode_responses=True,  # 将字节数据解码为字符串
    protocol=2,  # 兼容 Redis 5；Redis 6 及以上可使用 RESP3
)

# 设置 和 读取（字符串 和 列表或字典） “[{}]”
# 读取 ： 字符串
async def get_cache(key: str) :
    #return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None

# 读取 ： 列表或字典
async def get_json_cache(key: str) :
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data) # 序列化 解析 JSON 数据
        return None
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None


# 设置缓存 setex(key,expire,value)
async def set_cache(key: str, value: Any, expire: int = 3600) :
    try:
        if isinstance(value, dict) or isinstance(value, list):
            #转字符串再存
            value = json.dumps(value,ensure_ascii=False) # 中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
