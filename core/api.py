import requests

class PoeNinjaAPI:
    def __init__(self, league):
        self.league = league
        self.session = requests.Session()
        # Conforme a documentação oficial do poe.ninja-API-Document
        self.base_url = "https://poe.ninja/api/data"

    def get_data(self, category):
        """Diferencia entre Currency (pay/receive) e Item (chaosValue)"""
        # Scarabs são 'itemoverview', Moedas/Fragmentos são 'currencyoverview'
        resource = "itemoverview" if category == "Scarab" else "currencyoverview"
        
        url = f"{self.base_url}/{resource}?league={self.league}&type={category}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar {category}: {e}")
            return None

    def get_divine_price(self):
        """Busca o preço do Divine usando o novo método get_data"""
        data = self.get_data("Currency")
        
        if not data or 'lines' not in data:
            raise ConnectionError("Não foi possível obter dados para o preço do Divine.")

        for item in data['lines']:
            if item.get('currencyTypeName') == 'Divine Orb':
                # O preço de 'receive' é o valor de venda (mais realista para arbitragem)
                price = item.get('receive', {}).get('value')
                if price:
                    return price
        
        raise ValueError("Divine Orb não encontrado na API.")