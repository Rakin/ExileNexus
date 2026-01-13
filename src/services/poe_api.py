import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class PoeProfileClient:
    def __init__(self, account_name: str, session_id: str = None):
        self.account = account_name
        self.session_id = session_id or os.getenv("POESESSID")
        self.session = requests.Session()
        
        # Headers mais densos para evitar o "Forbidden"
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://www.pathofexile.com/account/view-profile/{account_name}"
        })

    def get_character_items(self, char_name: str) -> Dict[str, Any]:
        # Em 2026, a GGG exige o uso de POST para esta rota específica por segurança
        url = "https://www.pathofexile.com/character-window/get-items"
        
        payload = {
            "accountName": self.account,
            "character": char_name,
            "league": "Pohx Keepers Restart (PL77970)"
        }
        
        if self.session_id:
            # Garantir que o cookie seja setado corretamente para o domínio
            self.session.cookies.set("POESESSID", self.session_id.strip(), domain="pathofexile.com")

        try:
            # Trocando para POST - Muitas vezes resolve o Forbidden
            response = self.session.post(url, data=payload, timeout=15)
            
            # Se ainda der 403, tentamos uma última vez com GET
            if response.status_code == 403:
                response = self.session.get(url, params=payload, timeout=15)
            
            data = response.json()
            if "error" in data:
                print(f"❌ Resposta GGG: {data['error'].get('message', 'Acesso Negado')}")
            
            return data
        except Exception as e:
            return {"error": {"message": str(e)}}

    def extract_equipped_gems(self, items_data: Dict[str, Any]) -> List[str]:
        gems = []
        if "items" not in items_data:
            return []
        for item in items_data["items"]:
            for key in ["socketedItems", "abyssalSlots"]:
                for socketed in item.get(key, []):
                    if isinstance(socketed, dict):
                        name = socketed.get("typeLine")
                        if name:
                            gems.append(name)
        return list(set(gems))