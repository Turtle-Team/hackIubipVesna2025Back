import redis


class Redis:
    def __init__(self):
        self.r = redis.Redis(
            host='45.155.207.232',
            port=6379,
            password='epz9F6Nps3spBhiCvBRkUQ9SC4ka6kge',
            decode_responses=True
        )

    def get_value(self, key: str):
        value = self.r.get(key)
        return value

    def set_value(self, key: str, value: str):
        self.r.set(key, value)

    def ping(self):
        return self.r.ping()
