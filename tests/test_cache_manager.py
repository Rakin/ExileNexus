import time
from src.services.cache_manager import PriceCache

def test_cache_should_be_invalid_after_expiry():
    # Arrange
    # Criamos um cache que expira em apenas 1 segundo para testar rápido
    cache = PriceCache(expiry_seconds=1) 
    
    # Act
    # Mudamos 'update' para 'set' para coincidir com a nova arquitetura
    cache.set("Currency", {"divine": 200}) 
    time.sleep(1.1) # Esperamos o tempo de expiração
    
    # Assert
    assert cache.is_valid("Currency") is False

def test_cache_should_return_none_if_key_not_exists():
    # Arrange
    cache = PriceCache()
    
    # Assert
    assert cache.get("NonExistent") is None