import requests

class PoeNinjaAPI:
    def __init__(self, league):
        self.league = league
        self.base_url = "https://poe.ninja/api/data"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def get_currency_data(self, data_type):
        """
        Esta é a função que o main.py está procurando.
        Endpoint de referência: currencyoverview
        """
        url = f"{self.base_url}/currencyoverview?league={self.league}&type={data_type}"
        return self._fetch(url)

    def get_item_data(self, data_type):
        """Endpoint para itens (DivCards, Scarabs, etc)"""
        url = f"{self.base_url}/itemoverview?league={self.league}&type={data_type}"
        return self._fetch(url)

    def _fetch(self, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return r.json() if r.status_code == 200 else None
        except Exception as e:
            print(f"Erro de conexão na API: {e}")
            return None

    def get_divine_price(self):
        """Busca o preço do Divine ou levanta erro se a API falhar"""
        data = self.get_currency_data("Currency")
        
        if not data or 'lines' not in data:
            raise ConnectionError("Falha crítica: Não foi possível obter dados da API poe.ninja.")

        for item in data['lines']:
            if item.get('currencyTypeName') == 'Divine Orb':
                price = item.get('receive', {}).get('value')
                if price:
                    return price
        
        # Se percorreu tudo e não achou o Divine Orb (raro, mas possível em erro de liga)
        raise ValueError("Falha crítica: Divine Orb não encontrado nos dados da liga atual.")