import base64
import json
import requests
from typing import Dict, Any, Optional

class PoeNinjaClient:
    """
    Cliente para a API do poe.ninja.
    Regra: Utiliza JSON e descodifica Base64 quando necessário.
    """
    BASE_URL = "https://poe.ninja/api/data"

    def __init__(self, league: str = "Settlers"): # Ajuste para a liga atual
        self.league = league
        self.session = requests.Session()

    def get_prices(self, category: str) -> Dict[str, Any]:
        """
        Busca preços de uma categoria (ex: 'itemoverview' ou 'currencyoverview').
        """
        url = f"{self.BASE_URL}/{category}"
        params = {"league": self.league}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return self._process_response(response)
        except requests.RequestException as e:
            print(f"Erro ao contactar poe.ninja: {e}")
            return {"lines": []}

    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Garante que o retorno seja o JSON descodificado.
        """
        data = response.json()
        
        # Se os dados vierem em Base64 conforme as suas especificações
        if isinstance(data, str):
            return self._decode_base64_json(data)
            
        return data

    def _decode_base64_json(self, encoded_str: str) -> Dict[str, Any]:
        """Descodifica string Base64 para dicionário JSON."""
        decoded_bytes = base64.b64decode(encoded_str)
        return json.loads(decoded_bytes)