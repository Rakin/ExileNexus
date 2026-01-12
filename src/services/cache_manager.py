import time
from typing import Dict, Any, Optional

class PriceCache:
    """
    Gerencia o cache em memória para evitar excesso de chamadas à API.
    """
    def __init__(self, expiry_seconds: int = 3600): # 1 hora
        self._storage: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._expiry = expiry_seconds

    def is_valid(self, key: str) -> bool:
        """Verifica se o cache ainda não expirou."""
        if key not in self._storage:
            return False
        return (time.time() - self._timestamps[key]) < self._expiry

    def set(self, key: str, data: Any):
        self._storage[key] = data
        self._timestamps[key] = time.time()

    def get(self, key: str) -> Optional[Any]:
        return self._storage.get(key) if self.is_valid(key) else None