import hashlib
import json
import pickle
import os
import time
from typing import Any, Optional, Dict
from functools import wraps
import tempfile

class CacheManager:
    """
    Cache manager for storing and retrieving analysis results and model predictions.
    Supports both memory and disk-based caching with TTL (time-to-live) support.
    """
    
    def __init__(self, cache_dir: Optional[str] = None, default_ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory for disk cache (uses temp dir if None)
            default_ttl: Default TTL in seconds (1 hour)
        """
        self.cache_dir = cache_dir or os.path.join(tempfile.gettempdir(), 'compliance_cache')
        self.default_ttl = default_ttl
        self._memory_cache = {}
        
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate a unique cache key from arguments."""
        # Create a string representation of all arguments
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        
        # Generate MD5 hash
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, timestamp: float, ttl: int) -> bool:
        """Check if cache entry is expired."""
        return time.time() - timestamp > ttl
    
    def get_from_memory(self, key: str) -> Optional[Any]:
        """Get item from memory cache."""
        if key in self._memory_cache:
            data, timestamp, ttl = self._memory_cache[key]
            if not self._is_expired(timestamp, ttl):
                return data
            else:
                # Remove expired entry
                del self._memory_cache[key]
        return None
    
    def set_in_memory(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Set item in memory cache."""
        ttl = ttl or self.default_ttl
        self._memory_cache[key] = (data, time.time(), ttl)
    
    def get_from_disk(self, key: str) -> Optional[Any]:
        """Get item from disk cache."""
        cache_file = os.path.join(self.cache_dir, f"{key}.cache")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                data, timestamp, ttl = cached_data
                if not self._is_expired(timestamp, ttl):
                    return data
                else:
                    # Remove expired file
                    os.remove(cache_file)
            except (pickle.PickleError, OSError):
                # Handle corrupted cache files
                try:
                    os.remove(cache_file)
                except OSError:
                    pass
        
        return None
    
    def set_on_disk(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Set item in disk cache."""
        ttl = ttl or self.default_ttl
        cache_file = os.path.join(self.cache_dir, f"{key}.cache")
        
        try:
            cached_data = (data, time.time(), ttl)
            with open(cache_file, 'wb') as f:
                pickle.dump(cached_data, f)
        except (pickle.PickleError, OSError):
            # Silently fail if caching fails
            pass
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache (checks memory first, then disk)."""
        # Try memory cache first
        data = self.get_from_memory(key)
        if data is not None:
            return data
        
        # Try disk cache
        data = self.get_from_disk(key)
        if data is not None:
            # Store in memory for faster access
            self.set_in_memory(key, data)
            return data
        
        return None
    
    def set(self, key: str, data: Any, ttl: Optional[int] = None, disk: bool = True) -> None:
        """Set item in cache."""
        # Always set in memory
        self.set_in_memory(key, data, ttl)
        
        # Optionally set on disk
        if disk:
            self.set_on_disk(key, data, ttl)
    
    def invalidate(self, key: str) -> None:
        """Remove item from both memory and disk cache."""
        # Remove from memory
        if key in self._memory_cache:
            del self._memory_cache[key]
        
        # Remove from disk
        cache_file = os.path.join(self.cache_dir, f"{key}.cache")
        try:
            os.remove(cache_file)
        except OSError:
            pass
    
    def clear_all(self) -> None:
        """Clear all cache entries."""
        # Clear memory
        self._memory_cache.clear()
        
        # Clear disk
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except OSError:
            pass
    
    def cleanup_expired(self) -> int:
        """Remove expired entries from disk cache. Returns number of removed files."""
        removed_count = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    cache_file = os.path.join(self.cache_dir, filename)
                    try:
                        with open(cache_file, 'rb') as f:
                            cached_data = pickle.load(f)
                        
                        _, timestamp, ttl = cached_data
                        if self._is_expired(timestamp, ttl):
                            os.remove(cache_file)
                            removed_count += 1
                    
                    except (pickle.PickleError, OSError):
                        # Remove corrupted files
                        try:
                            os.remove(cache_file)
                            removed_count += 1
                        except OSError:
                            pass
        except OSError:
            pass
        
        return removed_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            'memory_entries': len(self._memory_cache),
            'disk_entries': 0,
            'cache_dir': self.cache_dir,
            'total_size_bytes': 0
        }
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    stats['disk_entries'] += 1
                    cache_file = os.path.join(self.cache_dir, filename)
                    stats['total_size_bytes'] += os.path.getsize(cache_file)
        except OSError:
            pass
        
        return stats

# Global cache instance
_global_cache = None

def get_cache_manager(cache_dir: Optional[str] = None, default_ttl: int = 3600) -> CacheManager:
    """Get or create global cache manager instance."""
    global _global_cache
    
    if _global_cache is None:
        _global_cache = CacheManager(cache_dir, default_ttl)
    
    return _global_cache

def cached(ttl: Optional[int] = None, disk: bool = True, key_prefix: str = ""):
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time to live in seconds
        disk: Whether to store on disk
        key_prefix: Prefix for cache key
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache_manager()
            
            # Generate cache key
            key_data = f"{key_prefix}:{func.__name__}:{args}:{sorted(kwargs.items())}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl, disk)
            
            return result
        
        return wrapper
    return decorator

def cache_compliance_results(method: str, content_hash: str, results: Dict, ttl: int = 3600):
    """Cache compliance analysis results."""
    cache = get_cache_manager()
    key = f"compliance:{method}:{content_hash}"
    cache.set(key, results, ttl, disk=True)

def get_cached_compliance_results(method: str, content_hash: str) -> Optional[Dict]:
    """Get cached compliance analysis results."""
    cache = get_cache_manager()
    key = f"compliance:{method}:{content_hash}"
    return cache.get(key)

def cache_model_embeddings(model_name: str, text_hash: str, embeddings: Any, ttl: int = 86400):
    """Cache model embeddings (24 hour TTL by default)."""
    cache = get_cache_manager()
    key = f"embeddings:{model_name}:{text_hash}"
    cache.set(key, embeddings, ttl, disk=True)

def get_cached_model_embeddings(model_name: str, text_hash: str) -> Optional[Any]:
    """Get cached model embeddings."""
    cache = get_cache_manager()
    key = f"embeddings:{model_name}:{text_hash}"
    return cache.get(key)

def cache_document_embeddings(model_name: str, content_hash: str, embeddings: Any, ttl: int = 86400):
    """Cache document embeddings."""
    cache = get_cache_manager()
    key = f"doc_embeddings:{model_name}:{content_hash}"
    cache.set(key, embeddings, ttl, disk=True)

def get_cached_document_embeddings(model_name: str, content_hash: str) -> Optional[Any]:
    """Get cached document embeddings."""
    cache = get_cache_manager()
    key = f"doc_embeddings:{model_name}:{content_hash}"
    return cache.get(key)

def get_content_hash(content: str) -> str:
    """Generate a hash for content to use as cache key."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]  # Use first 16 chars

def cache_iso_standards(standards: Dict, ttl: int = 86400 * 7):
    """Cache ISO standards (7-day TTL by default)."""
    cache = get_cache_manager()
    key = "iso_standards_27002"
    cache.set(key, standards, ttl, disk=True)

def get_cached_iso_standards() -> Optional[Dict]:
    """Get cached ISO standards."""
    cache = get_cache_manager()
    key = "iso_standards_27002"
    return cache.get(key)


def setup_cache_cleanup_task():
    """Setup periodic cache cleanup (call this in app initialization)."""
    import threading
    import time
    
    def cleanup_worker():
        while True:
            time.sleep(3600)  # Run every hour
            try:
                cache = get_cache_manager()
                removed = cache.cleanup_expired()
                if removed > 0:
                    print(f"Cleaned up {removed} expired cache entries")
            except Exception:
                pass  # Silently handle cleanup errors
    
    cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
    cleanup_thread.start()