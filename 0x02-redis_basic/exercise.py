#!/usr/bin/env python3
""" Exercise file """

import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a method is called.

    Args:
        method (callable): The method to count the number of calls.

    Returns:
        callable: A wrapper function that counts the number of calls.
    """

    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that counts the number of calls.

        Args:
            self: The instance of the class.
            *args: The arguments passed to the method.
            **kwargs: The keyword arguments passed to the method.

        Returns:
            The result of the method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs for a method.

    Args:
        method (callable): The method to store the history.

    Returns:
        callable: A wrapper function that stores the history.
    """

    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores the history.

        Args:
            self: The instance of the class.
            *args: The arguments passed to the method.
            **kwargs: The keyword arguments passed to the method.

        Returns:
            The result of the method.
        """
        self._redis.rpush(f"{key}:inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{key}:outputs", str(result))
        return result

    return wrapper


def replay(method: Callable):
    """
    Displays the history of calls of a method.

    Args:
        method (callable): The method to display the history.
    """
    key = method.__qualname__
    redis = method.__self__._redis
    count = redis.get(key).decode('utf-8')
    inputs = redis.lrange(f"{key}:inputs", 0, -1)
    outputs = redis.lrange(f"{key}:outputs", 0, -1)

    print(f"{key} was called {count} times:")
    for i, o in zip(inputs, outputs):
        print(f"{key}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """ Cache class """
    def __init__(self):
        """
        Initializes the Cache class with a Redis client instance
        and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key (UUID)
        and stores the input data in Redis using the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The generated key used to store the data in Redis.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float]:
        """
        Retrieves the data stored in Redis identified by key.

        Args:
            key (str): The key used to identify the data in Redis.
            fn (callable): A callable function to transform the data.

        Returns:
            Union[str, bytes, int, float]: The data stored in Redis.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves the data stored in Redis identified by key as a string.

        Args:
            key (str): The key used to identify the data in Redis.

        Returns:
            Union[str, None]: The data stored in Redis as a string.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves the data stored in Redis identified by key as an integer.

        Args:
            key (str): The key used to identify the data in Redis.

        Returns:
            Union[int, None]: The data stored in Redis as an integer.
        """
        return self.get(key, fn=int)
