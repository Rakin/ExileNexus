import json
import os
from typing import List, Dict, Any

class PoeDataProcessor:
    """
    Processa dados brutos minerados para responder perguntas de build.
    Regra: Filtra gemas por classe (Templar/Inquisitor) e disponibilidade em quests.
    """
    def __init__(self, raw_dir: str = "data/raw"):
        self.raw_dir = raw_dir
        self.gems_data = self._load_json("gems.json")
        self.quest_data = self._load_json("quests.json")
        # No POE, Inquisitor herda de Templar (ID 3)
        self.templar_id = "Templar" 

    def _load_json(self, file_name: str) -> Dict[str, Any]:
            path = os.path.join(self.raw_dir, file_name)
            if not os.path.exists(path):
                print(f"⚠️ Aviso: Arquivo {file_name} não encontrado.")
                return {} # Retorna dicionário vazio em vez de estourar erro
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)

    def get_gems_by_act_and_class(self, act: int) -> List[Dict[str, Any]]:
        """
        Retorna gemas disponíveis para Templar no Ato especificado.
        Baseado nos links da poedb que você utiliza.
        """
        available_gems = []
        
        for gem_id, info in self.gems_data.items():
            # Filtra gemas que são recompensas ou vendidas para Templar
            # O RePoE estrutura isso dentro de 'static' ou 'rewards'
            if "rewards" in info:
                for reward in info["rewards"]:
                    if reward.get("character") == self.templar_id and reward.get("act") == act:
                        available_gems.append({
                            "name": info.get("base_item", {}).get("display_name", gem_id),
                            "required_level": info.get("required_level"),
                            "quest": reward.get("quest"),
                            "vendor": reward.get("vendor")
                        })
        
        return sorted(available_gems, key=lambda x: x['required_level'])

    def validate_item_requirement(self, char_level: int, item_req_level: int) -> bool:
        """Valida a regra de prerequisitos de nível."""
        return char_level >= item_req_level

    def get_quest_info(self, quest_id: str) -> Dict[str, Any]:
        """
        Retorna detalhes de uma quest minerada (Ato, Recompensa).
        Útil para saber se o Kinquisitor_PBD já passou por ela.
        """
        quests = self._load_json("quests.json")
        return quests.get(quest_id, {})