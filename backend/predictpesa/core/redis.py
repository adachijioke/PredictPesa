"""
Redis configuration and connection management for PredictPesa.
Handles caching, session storage, and real-time data.
"""

import json
from typing import Any, Optional, Union

import redis.asyncio as redis
import structlog

from predictpesa.core.config import settings

logger = structlog.get_logger(__name__)

# Global Redis connection pool
redis_pool: Optional[redis.ConnectionPool] = None
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection pool."""
    global redis_pool, redis_client
    
    try:
        redis_pool = redis.ConnectionPool.from_url(
            settings.redis_url,
            max_connections=settings.redis_pool_size,
            socket_timeout=settings.redis_socket_timeout,
            socket_connect_timeout=settings.redis_socket_connect_timeout,
            decode_responses=True,
        )
        
        redis_client = redis.Redis(connection_pool=redis_pool)
        
        # Test connection
        await redis_client.ping()
        logger.info("Redis connection established")
        
    except Exception as e:
        logger.error("Failed to initialize Redis", error=str(e))
        raise


async def close_redis() -> None:
    """Close Redis connections."""
    global redis_pool, redis_client
    
    if redis_client:
        await redis_client.close()
        redis_client = None
    
    if redis_pool:
        await redis_pool.disconnect()
        redis_pool = None
    
    logger.info("Redis connections closed")


def get_redis() -> redis.Redis:
    """
    Get Redis client instance.
    
    Returns:
        redis.Redis: Redis client
        
    Raises:
        RuntimeError: If Redis is not initialized
    """
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    
    return redis_client


class RedisCache:
    """Redis cache utility class."""
    
    def __init__(self, prefix: str = "predictpesa"):
        self.prefix = prefix
        self.client = get_redis()
    
    def _make_key(self, key: str) -> str:
        """Create prefixed cache key."""
        return f"{self.prefix}:{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            value = await self.client.get(self._make_key(key))
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning("Cache get failed", key=key, error=str(e))
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds
            
        Returns:
            True if successful
        """
        try:
            serialized = json.dumps(value, default=str)
            await self.client.set(
                self._make_key(key),
                serialized,
                ex=expire
            )
            return True
        except Exception as e:
            logger.warning("Cache set failed", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        try:
            await self.client.delete(self._make_key(key))
            return True
        except Exception as e:
            logger.warning("Cache delete failed", key=key, error=str(e))
            return False
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        try:
            return bool(await self.client.exists(self._make_key(key)))
        except Exception as e:
            logger.warning("Cache exists check failed", key=key, error=str(e))
            return False
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment counter in cache.
        
        Args:
            key: Cache key
            amount: Amount to increment
            
        Returns:
            New value or None
        """
        try:
            return await self.client.incrby(self._make_key(key), amount)
        except Exception as e:
            logger.warning("Cache increment failed", key=key, error=str(e))
            return None
    
    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration for key.
        
        Args:
            key: Cache key
            seconds: Expiration time in seconds
            
        Returns:
            True if successful
        """
        try:
            return bool(await self.client.expire(self._make_key(key), seconds))
        except Exception as e:
            logger.warning("Cache expire failed", key=key, error=str(e))
            return False


class RateLimiter:
    """Redis-based rate limiter."""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.client = redis_client or get_redis()
    
    async def is_allowed(
        self,
        key: str,
        limit: int,
        window: int
    ) -> tuple[bool, int]:
        """
        Check if request is allowed within rate limit.
        
        Args:
            key: Rate limit key (e.g., user_id, IP)
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        try:
            pipe = self.client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            results = await pipe.execute()
            
            current_count = results[0]
            
            if current_count <= limit:
                return True, limit - current_count
            else:
                return False, 0
                
        except Exception as e:
            logger.warning("Rate limit check failed", key=key, error=str(e))
            # Fail open - allow request if Redis is down
            return True, limit


# Global cache instance
cache = RedisCache()
rate_limiter = RateLimiter()
