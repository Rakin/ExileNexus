import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseDataProcessor(ABC):
    def __init__(self, filename: str):
        self.raw_path = os.path.join("data", "raw", filename)
        self.data = self._load_json()

    # src/extraction/base_processor.py - Atualize o método _load_json
    def _load_json(self) -> Dict[str, Any]:
        if not os.path.exists(self.raw_path):
            print(f"⚠️ Aviso: Arquivo {self.raw_path} não encontrado.")
            return {}
        # Mudança para utf-8-sig para lidar com BOM do Windows
        with open(self.raw_path, 'r', encoding='utf-8-sig') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Erro crítico: {self.raw_path} não é um JSON válido.")
                return {}


# src/extraction/processors/gem_processor.py - Atualize o método get_data
    def get_data(self, gem_name: str):
        """Busca metadados de uma gema específica com navegação segura."""
        for gem_id, info in self.data.items():
            # Verificamos se info é um dicionário e se tem base_item
            if isinstance(info, dict):
                base_item = info.get("base_item")
                if base_item and base_item.get("display_name", "").lower() == gem_name.lower():
                    return info
        return None