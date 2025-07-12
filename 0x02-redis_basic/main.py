#!/usr/bin/env python3
""" Main file to test Cache.store """
import redis
from exercise import Cache, replay
from web import get_page


cache = Cache()


TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    result = cache.get(key, fn=fn)
    assert result == value, f"Expected {value}, got {result}"
    print(f"{key}: {result}")

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))



cache.store(b"first")
print(cache.get(cache.store.__qualname__))  

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))  



s1 = cache.store("first")
s2 = cache.store("second")
s3 = cache.store("third")

inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

print("inputs:", inputs)
print("outputs:", outputs)



cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)


# web.py

url = "http://example.com"
content = get_page(url)
print(content)