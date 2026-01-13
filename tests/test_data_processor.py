import pytest
import os
from src.extraction.data_manager import ExileNexusData
from src.extraction.processors.gem_processor import GemProcessor
from src.extraction.processors.reward_processor import RewardProcessor

class TestModularProcessors:

    @pytest.fixture
    def data_manager(self):
        """Instancia o orquestrador principal."""
        return ExileNexusData()

    def test_gem_processor_lookup(self):
        """Valida se o GemProcessor encontra uma gema pelo nome."""
        proc = GemProcessor()
        # Testando com Smite (gema comum de Templar)
        gem_info = proc.get_data("Smite")
        
        # Se o gems.json existir e estiver populado, gem_info não será None
        if gem_info:
            assert "base_item" in gem_info
        else:
            pytest.skip("gems.json vazio ou Smite não encontrado para teste.")

    def test_reward_processor_act_1(self):
        """Valida se o RewardProcessor lê as recompensas do Ato 1 para Templar."""
        proc = RewardProcessor()
        rewards = proc.get_data("Templar", 1)
        
        assert isinstance(rewards, list)
        # De acordo com o nosso mock/manual que criamos anteriormente
        assert "Smite" in rewards

    def test_data_manager_integration(self, data_manager):
        """Testa o Facade (ExileNexusData) integrando os processadores."""
        gems_act_1 = data_manager.get_leveling_gems("Templar", 1)
        assert "Smite" in gems_act_1
        assert "Glacial Hammer" in gems_act_1

    def test_processor_file_not_found_resilience(self):
        """Garante que o sistema não quebra se o arquivo JSON não existir."""
        from src.extraction.base_processor import BaseDataProcessor
        
        class FakeProcessor(BaseDataProcessor):
            def get_data(self, **kwargs): return {}

        # Tentando carregar um arquivo que não existe
        proc = FakeProcessor("arquivo_inexistente.json")
        assert proc.data == {}