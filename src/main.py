# src/main.py
from services.poe_ninja_api import PoeNinjaClient
from services.cache_manager import PriceCache
from core.scanner import ItemScanner

def main():
    # Inicializa dependências
    cache = PriceCache(expiry=3600)
    api = PoeNinjaClient(cache=cache)
    scanner = ItemScanner(api=api)
    
    # Executa a lógica
    scanner.run()

if __name__ == "__main__":
    main()