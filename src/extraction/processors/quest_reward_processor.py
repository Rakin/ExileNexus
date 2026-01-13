from src.extraction.base_processor import BaseDataProcessor
from typing import List

class RewardProcessor(BaseDataProcessor):
    def __init__(self):
        # Ele herda o carregamento automático do base_processor.py
        super().__init__("quest_rewards.json")

    def get_data(self, class_name: str, act: int) -> List[str]:
        """
        Retorna a lista de gemas disponíveis para uma classe em um determinado ato.
        Estrutura esperada: {"QuestReward": {"Templar": {"1": ["Gema A", "Gema B"]}}}
        """
        if not self.data:
            return []
            
        # Navegação segura no JSON que mineramos
        all_rewards = self.data.get("QuestReward", {})
        class_rewards = all_rewards.get(class_name, {})
        
        # O ato é tratado como string no JSON (ex: "1")
        gems_in_act = class_rewards.get(str(act), [])
        
        return gems_in_act