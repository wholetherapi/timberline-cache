import time
from collections import OrderedDict


class TieredCache:
    def __init__(self, hot_size=1024, warm_size=8192, ttl_seconds=300):
        self.hot = OrderedDict()
        self.warm = OrderedDict()
        self.hot_size = hot_size
        self.warm_size = warm_size
        self.ttl = ttl_seconds

    def get(self, key, default=None):
        entry = self.hot.get(key) or self.warm.get(key)
        if entry is None:
            return default
        value, expires = entry
        if expires < time.time():
            self.hot.pop(key, None)
            self.warm.pop(key, None)
            return default
        return value

    def set(self, key, value):
        expires = time.time() + self.ttl
        if key in self.warm:
            self.warm.pop(key)
        self.hot[key] = (value, expires)
        self.hot.move_to_end(key)
        while len(self.hot) > self.hot_size:
            old_key, old_val = self.hot.popitem(last=False)
            self.warm[old_key] = old_val
        while len(self.warm) > self.warm_size:
            self.warm.popitem(last=False)

    def stats(self):
        return {"hot": len(self.hot), "warm": len(self.warm)}
