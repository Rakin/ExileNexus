from services.poe_ninja_api import PoeNinjaClient
from services.cache_manager import PriceCache

class ItemScanner:
    """
    Orquestra o scan de itens integrando a API e o Cache.
    """
    def __init__(self, api_client: PoeNinjaClient, cache: PriceCache):
        self.api = api_client
        self.cache = cache

    def get_item_price(self, item_name: str, category: str) -> float:
        # Guard Clause: Verifica cache primeiro
        if self.cache.is_valid(category):
            return self._find_in_data(self.cache.get(category), item_name)

        # Busca novos dados se o cache expirou
        data = self.api.fetch_data(category)
        self.cache.update(category, data)
        
        return self._find_in_data(data, item_name)

    def _find_in_data(self, data: Dict, item_name: str) -> float:
        # Lógica de busca otimizada
        for item in data.get('lines', []):
            if item.get('name') == item_name:
                return item.get('chaosValue', 0.0)
        return 0.0
    # ... (todo o código da classe ItemScanner aqui)