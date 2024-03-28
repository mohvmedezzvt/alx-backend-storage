#!/usr/bin/env python3
""" Exercise file """

import redis
import uuid
from typing import Union


class Cache:
    """ Cache class """
    def __init__(self) -> None:
        """
        Initializes the Cache class with a Redis client instance
        and flushes the Redis database.
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

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
