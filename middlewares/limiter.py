# middlewares/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

class CustomLimiter:
    def __init__(self):
        self.limiter = Limiter(key_func=get_remote_address)
        self.enabled = True

    def limit(self, limit_value: str):
        if self.enabled:
            return self.limiter.limit(limit_value)
        else:
            return lambda x: x

limiter = CustomLimiter()