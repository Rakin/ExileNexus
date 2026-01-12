import time
from typing import Dict, Any, Optional

class PriceCache:
    """
    Gerencia o cache local para evitar chamadas excessivas.
    Regra: Expira em 1 hora (3600 segundos).
    """
    def __init__(self, expiry_seconds: int = 3600):
        self._cache: Dict[str, Any] = {}
        self._expiry = expiry_seconds
        self._last_update: Dict[str, float] = {}

    def is_valid(self, key: str) -> bool:
        if key not in self._cache:
            return False
        return (time.time() - self._last_update[key]) < self._expiry

    def update(self, key: str, data: Any):
        self._cache[key] = data
        self._last_update[key] = time.time()

    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)