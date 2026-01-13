import os
import sys
from dotenv import load_dotenv
from src.services.poe_api import PoeProfileClient
from src.extraction.data_manager import ExileNexusData

# Carrega o POESESSID do arquivo .env
load_dotenv()

def run_generic_audit(account: str, char_name: str, act: int):
    # Recupera o token de sessão
    session_id = os.getenv("POESESSID")
    
    # Inicia o cliente com a sessão autenticada
    client = PoeProfileClient(account_name=account, session_id=session_id)
    nexus = ExileNexusData()
    
    print(f"\n--- ExileNexus: Auditando {char_name} ---")
    
    # Agora a chamada deve retornar 200 OK em vez de 403
    profile_data = client.get_character_items(char_name)
    # Adicione isso para debugarmos o JSON real
    if profile_data:
        print(f"DEBUG: Chaves recebidas do perfil: {list(profile_data.keys())}")
        if "character" in profile_data:
            print(f"DEBUG: Dados do Char: {profile_data['character']}")
            
    if not profile_data:
        print("❌ Erro: Falha na autenticação. Verifique o seu POESESSID no arquivo .env")
        return

    # Resto da lógica de auditoria...
    current_class = profile_data.get("character", {}).get("class", "Unknown")
    # (Mapeamento de ascendência para classe base que fizemos anteriormente)
    class_map = {"Inquisitor": "Templar", "Hierophant": "Templar", "Guardian": "Templar"}
    base_class = class_map.get(current_class, current_class)

    equipped_gems = client.extract_equipped_gems(profile_data)
    available_rewards = []
    for a in range(1, act + 1):
        available_rewards.extend(nexus.rewards.get_data(base_class, a))
    
    missing = [g for g in available_rewards if g not in equipped_gems]
    
    print(f"Status: Autenticado como {account}")
    print(f"Classe: {current_class} | Gemas Detectadas: {len(equipped_gems)}")
    
    if missing:
        print(f"⚠️ Gemas faltando no Ato {act}: {missing}")
    else:
        print(f"✅ Build sincronizada com o Ato {act}!")

if __name__ == "__main__":
    acc = sys.argv[1] if len(sys.argv) > 1 else "Kushim78-0201"
    char = sys.argv[2] if len(sys.argv) > 2 else "Kinquisitor_PBD"
    target_act = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    run_generic_audit(acc, char, target_act)