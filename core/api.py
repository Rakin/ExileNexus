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
        """
        Utiliza a função get_currency_data para extrair 
        o valor atual do Divine em Chaos.
        """
        data = self.get_currency_data("Currency")
        if data and 'lines' in data:
            for item in data['lines']:
                if item.get('currencyTypeName') == 'Divine Orb':
                    # Retorna o valor de venda (receive) do Divine
                    return item.get('receive', {}).get('value', 194)
        return 194 # Fallback caso a API falhe