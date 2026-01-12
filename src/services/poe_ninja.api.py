import base64
import json
from typing import Dict, Any

class PoeNinjaClient:
    """
    Responsável estritamente pela comunicação com a API do poe.ninja.
    Segue a regra de converter Base64 para JSON.
    """
    BASE_URL = "https://poe.ninja/api/data"

    def __init__(self, session):
        self.session = session

    def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        response = self.session.get(f"{self.BASE_URL}/{endpoint}")
        response.raise_for_status()
        
        # Simulação da regra: extrair Base64 e converter para JSON
        # conforme suas diretrizes de usar sempre o JSON.
        data = response.json()
        if 'encoded_data' in data:
            return self._decode_base64_json(data['encoded_data'])
        return data

    def _decode_base64_json(self, encoded_str: str) -> Dict[str, Any]:
        decoded_bytes = base64.b64decode(encoded_str)
        return json.loads(decoded_bytes)