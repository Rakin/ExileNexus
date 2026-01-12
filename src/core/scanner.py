from src.services.poe_ninja_api import PoeNinjaClient
from src.services.cache_manager import PriceCache

class ItemScanner:
    """
    Lógica principal do scanner aplicando SOLID e Clean Code.
    """
    def __init__(self, api: PoeNinjaClient, cache: PriceCache):
        self.api = api
        self.cache = cache

    def fetch_item_value(self, item_name: str, category: str = "itemoverview") -> float:
        """
        Retorna o valor em Chaos de um item específico.
        """
        # Guard Clause: Se estiver no cache, retorna imediatamente
        cached_data = self.cache.get(category)
        if cached_data:
            return self._extract_price(cached_data, item_name)

        # Se não, busca na API e atualiza cache
        data = self.api.get_prices(category)
        self.cache.set(category, data)
        
        return self._extract_price(data, item_name)

    def _extract_price(self, data: dict, item_name: str) -> float:
        """Procura o item na lista de resultados."""
        for item in data.get("lines", []):
            if item.get("name") == item_name:
                return float(item.get("chaosValue", 0.0))
        return 0.0