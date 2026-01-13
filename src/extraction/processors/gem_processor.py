from src.extraction.base_processor import BaseDataProcessor

class GemProcessor(BaseDataProcessor):
    def __init__(self):
        super().__init__("gems.json")

    def get_data(self, gem_name: str):
        """Busca metadados de uma gema específica com proteção contra nulos."""
        if not self.data:
            return None
            
        for gem_id, info in self.data.items():
            # Proteção: verifica se info é um dicionário antes de dar .get()
            if isinstance(info, dict):
                base_item = info.get("base_item")
                # Proteção: verifica se base_item existe e é um dicionário
                if isinstance(base_item, dict):
                    display_name = base_item.get("display_name", "")
                    if display_name.lower() == gem_name.lower():
                        return info
        return None