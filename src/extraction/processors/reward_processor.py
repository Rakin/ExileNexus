from src.extraction.base_processor import BaseDataProcessor

class RewardProcessor(BaseDataProcessor):
    def __init__(self):
        super().__init__("quest_rewards.json")

    def get_data(self, class_name: str, act: int):
        """Busca gemas de recompensa por classe e ato."""
        rewards = self.data.get("QuestReward", {}).get(class_name, {})
        return rewards.get(str(act), [])