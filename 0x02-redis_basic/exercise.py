#!/usr/bin/env python3
""" Task 0: Basic Redis store """
import redis
import uuid
from typing import Union
from typing import Callable, Optional, Any
import functools


def count_calls(method: Callable) -> Callable:
        """Decorator to count how many times a method is called"""
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store inputs and outputs of method calls in Redis"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key_input = f"{method.__qualname__}:inputs"
        key_output = f"{method.__qualname__}:outputs"

        self._redis.rpush(key_input, str(args))  # Store inputs
        result = method(self, *args, **kwargs)    # Execute original method
        self._redis.rpush(key_output, str(result))  # Store output

        return result
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls to a method"""
    redis_instance = method.__self__._redis
    qualname = method.__qualname__

    inputs_key = f"{qualname}:inputs"
    outputs_key = f"{qualname}:outputs"

    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    print(f"{qualname} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(f"{qualname}(*{input_.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    def __init__(self):
        """Initialize Redis connection and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis using a random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    from typing import Callable, Optional, Any



    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Retrieve key from Redis and optionally convert type"""
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)



    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key