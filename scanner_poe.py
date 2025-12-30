import requests
import time
import os
import json
import winsound

def detectar_liga_atual():
    """Tenta detectar a liga através do endpoint de builds ou assume Standard"""
    try:
        # Este link retorna as ligas que possuem personagens ativos no ranking
        url = "https://poe.ninja/api/data/getbuildleagues"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            ligas = r.json() # Retorna uma lista simples: ["Settlers", "Standard", ...]
            # Filtra para pegar a primeira que não seja Standard/Hardcore
            temporarias = [l for l in ligas if l not in ["Standard", "Hardcore", "SSF Standard"]]
            if temporarias:
                return temporarias[0]
    except:
        pass
    return "Standard"

def buscar_dados(liga, tipo_endpoint, tipo_data):
    url = f"https://poe.ninja/api/data/{tipo_endpoint}?league={liga}&type={tipo_data}"
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except: return None

def main():
    while True:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f: config = json.load(f)
        else:
            config = {"league": "auto", "min_profit_percent": 5}

        liga = config.get("league", "auto")
        if liga == "auto": liga = detectar_liga_atual()
        min_percent = config.get("min_profit_percent", 5)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"--- PoE REAL ARBITRAGE SCANNER ---")
        print(f"Liga: {liga} | Horário: {time.strftime('%H:%M:%S')}")
        print(f"Filtro: Apenas itens acima de 1.0 Chaos (Evitando erros)\n")

        alvos = [
            ("currencyoverview", "Currency"),
            ("currencyoverview", "Fragment")
        ]

        for endpoint, tipo in alvos:
            data = buscar_dados(liga, endpoint, tipo)
            if not data: continue

            print(f"--- Categoria: {tipo} ---")
            for item in data['lines']:
                nome = item.get('currencyTypeName') or item.get('name')
                pay_val = item.get('pay', {}).get('value')
                rec_val = item.get('receive', {}).get('value')

                # FILTRO DE REALIDADE:
                # 1. O preço de compra (Pay) deve ser pelo menos 1 Chaos.
                # 2. A margem deve ser lógica (entre 1% e 50%). Mais que 50% em currency costuma ser erro.
                if pay_val and pay_val >= 1.0 and rec_val:
                    lucro_percent = ((rec_val / pay_val) - 1) * 100
                    
                    if min_percent <= lucro_percent <= 50:
                        print(f"[LUCRO] {nome:25}")
                        print(f"      Compra: {pay_val:>8.2f}c | Venda: {rec_val:>8.2f}c | Margem: {lucro_percent:>5.2f}%")
                        
                        if lucro_percent >= min_percent:
                            winsound.Beep(1000, 200)
        
        print(f"\nVarredura concluída. Próxima em 1 hora...")
        time.sleep(3600)

if __name__ == "__main__":
    main()