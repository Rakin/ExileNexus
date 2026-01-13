from src.extraction.processors.gem_processor import GemProcessor
from src.extraction.processors.reward_processor import RewardProcessor

class ExileNexusData:
    def __init__(self):
        # Cada objeto trabalha com seu próprio JSON
        self.gems = GemProcessor()
        self.rewards = RewardProcessor()
        # No futuro: self.mods = ModProcessor()

    def get_leveling_gems(self, char_class: str, act: int):
        """Exemplo de uso: Combina os dados de recompensas."""
        return self.rewards.get_data(char_class, act)