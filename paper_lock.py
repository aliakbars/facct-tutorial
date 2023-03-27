from pottery import Redlock
from redis import Redis

class PaperLock:
    def lock(self, id: int) -> bool:
        pass

    def unlock(self, id: int) -> bool:
        pass

class RedisPaperLock(PaperLock):
    _instance = None

    @staticmethod
    def get():
        """ Singleton pattern to instantiate RedisPaperLock
        """
        if not RedisPaperLock._instance:
            RedisPaperLock._instance = RedisPaperLock()
        
        return RedisPaperLock._instance
        
    def __init__(self, redis_url="redis://localhost:6379/1", base_lock_key="paper_lock") -> None:
        self._redis = Redis.from_url(redis_url)
        self._base_lock_key = base_lock_key
        self._paper_lock = {}

    def lock(self, id: int) -> bool:
        if id in self._paper_lock:
            return False
        
        redis_lock = Redlock(key=self._lock_key(id), masters={self._redis}, auto_release_time=1)
        self._paper_lock[id] = redis_lock
        return redis_lock.acquire()

    def unlock(self, id: int) -> bool:
        if id not in self._paper_lock:
            return False
        
        redis_lock = Redlock(key=self._lock_key(id), masters={self._redis}, auto_release_time=1)
        if redis_lock.locked:
            redis_lock.release()
            del self._paper_lock[id]
            return True
        return False

    def _lock_key(self, id: int) -> str:
        return f"{self._base_lock_key}|{id}"