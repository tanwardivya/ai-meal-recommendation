from typing import Any

from expiringdict import ExpiringDict
from loguru import logger
class InMemoryCache:
    cache: ExpiringDict
    
    @staticmethod
    def startup() -> None:
        InMemoryCache.cache = ExpiringDict(max_len=100, max_age_seconds=3600)
        logger.info('Inmemory cache is created')
    
    @staticmethod
    def get(key:str):
        return InMemoryCache.cache.get(key, default=None)
    
    @staticmethod
    def create(key: str, value: Any):
        item = InMemoryCache.get(key)
        if item is None:
            InMemoryCache.cache[key] = value