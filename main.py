import os
import time
import json
import winsound
from core.api import PoeNinjaAPI
from core.analyzer import ProfitAnalyzer

class PoeScannerApp:
    def __init__(self):
        self.config_path = 'config.json'

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except:
            return {"league": "Standard", "min_profit_percent": 1, "intervalo_segundos": 60, "debug": False}

    # --- A FUNÇÃO QUE ESTAVA FALTANDO ESTÁ AQUI EMBAIXO ---
    def format_currency(self, chaos_amount, divine_price):
        """Converte Chaos para Divine se for maior que 1 Div, senão mostra Chaos"""
        if chaos_amount >= divine_price:
            div_val = chaos_amount / divine_price
            return f"{div_val:.2f} div"
        return f"{chaos_amount:.1f}c"

    def run(self):
        while True:
            cfg = self.load_config()
            os.system('cls' if os.name == 'nt' else 'clear')
            
            api = PoeNinjaAPI(cfg['league'])
            divine_price = api.get_divine_price()
            
            print(f"--- POE SCANNER PRO ---")
            print(f"Liga: {cfg['league']} | 1 Divine = {divine_price:.1f} Chaos\n")
            
            all_ops = []
            categories = ["Currency", "Fragment", "Scarab"]
            
            for cat in categories:
                data = api.get_currency_data(cat)
                if data and 'lines' in data:
                    print(f"[LOG] Analisando {len(data['lines'])} itens em {cat}...") # Adicione esta linha
                    ops = ProfitAnalyzer.scan_currencies(
                        data, 
                        cfg['min_profit_percent'], 
                        cfg.get('min_profit_chaos', 10.0), # Este é o argumento que faltava!
                        cfg['debug'], 
                        divine_price
                    )
                    if ops:
                        all_ops.extend(ops)

            if all_ops:
                # Ordena as oportunidades pelo lucro bruto (Chaos)
                all_ops.sort(key=lambda x: x['profit_chaos'], reverse=True)
                
                print(f"{'ITEM':<22} | {'PROFIT':<8} | {'TREND':<7} | {'LUCRO'}")
                print("-" * 65)
                for op in all_ops:
                    trend_arrow = "↑" if op['trend'] > 0 else "↓"
                    lucro_formatado = self.format_currency(op['profit_chaos'], divine_price)
                    
                    # Ícone de risco baseado na nova lógica anti-price fixing
                    status_icon = "⚠️" if op['risk'] == "ALTO" else " "
                    
                    print(f"{op['name']:22} | {op['profit_pct']:>6.2f}% | {trend_arrow} {abs(op['trend']):>4.0f}% | {lucro_formatado} {status_icon}")
                    
                    if op['profit_pct'] >= 5:
                        winsound.Beep(1000, 200)
            else:
                print("Buscando oportunidades lucrativas (Currency & Fragment)...")

            print(f"\nPróxima varredura em {cfg['intervalo_segundos']}s...")
            time.sleep(cfg['intervalo_segundos'])

if __name__ == "__main__":
    PoeScannerApp().run()