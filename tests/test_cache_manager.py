import time
from src.services.cache_manager import PriceCache

def test_cache_should_be_invalid_after_expiry():
    # Arrange (Organiza)
    cache = PriceCache(expiry_seconds=1) # Cache curto para o teste
    cache.update("Currency", {"divine": 200})
    
    # Act (Age)
    time.sleep(1.1)
    valid = cache.is_valid("Currency")
    
    # Assert (Afirma)
    assert valid is False

def test_cache_should_return_none_if_key_not_exists():
    cache = PriceCache()
    assert cache.get("NonExistent") is None