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
            api = PoeNinjaAPI(cfg['league'])
            
            try:
                divine_price = api.get_divine_price()
                all_ops = []
                categories = ["Currency", "Fragment", "Scarab"]
                
                # 1. COLETA DE DADOS (Loop silencioso)
                for cat in categories:
                    data = api.get_data(cat)
                    if data and 'lines' in data:
                        # Log discreto para sabermos o progresso
                        print(f"[LOG] Coletando {len(data['lines'])} itens em {cat}...")
                        
                        ops = ProfitAnalyzer.scan_currencies(
                            data, 
                            cfg['min_profit_percent'], 
                            cfg.get('min_profit_chaos', 10.0), 
                            cfg['debug'], 
                            divine_price,
                            cat
                        )
                        if ops:
                            all_ops.extend(ops)

                # 2. LIMPEZA E EXIBIÇÃO ÚNICA (Fora do loop das categorias)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"--- POE SCANNER PRO ---")
                print(f"Liga: {cfg['league']} | 1 Divine = {divine_price:.1f} Chaos\n")
                
                if all_ops:
                    # Ordenação Inteligente
                    all_ops.sort(key=lambda x: (x['risk'] != 'BAIXO', -x['profit_chaos']))
                    
                    print(f"{'ITEM':<22} | {'CATEGORIA':<10} | {'LUCRO':<10} | {'TREND'}")
                    print("-" * 75)
                    
                    for op in all_ops[:20]:
                        lucro_str = self.format_currency(op['profit_chaos'], divine_price)
                        trend_arrow = "↑" if op['trend'] > 0 else "↓"
                        icon = "💎" if op['profit_chaos'] > divine_price else ("  ")
                        if op['risk'] == "ALTO": icon = "⚠️"

                        print(f"{op['name']:22} | {op['category']:<10} | {lucro_str:<10} | {trend_arrow} {abs(op['trend']):>2.0f}% {icon}")
                    
                    # 3. RESUMO FINAL (Abaixo da tabela consolidada)
                    total_itens = len(all_ops)
                    joias = len([x for x in all_ops if x['profit_chaos'] > divine_price])
                    
                    print("-" * 75)
                    print(f"📊 RESUMO FINAL DA VARREDURA:")
                    print(f"   - Total de oportunidades: {total_itens}")
                    print(f"   - Itens de alto lucro (💎): {joias}")
                    if all_ops:
                        print(f"   - Sniper Sugerido: {all_ops[0]['name']} ({all_ops[0]['category']})")
                else:
                    print("\n[!] Nenhuma oportunidade lucrativa encontrada no momento.")

            except Exception as e:
                print(f"⚠️ Erro na varredura: {e}")

            print(f"\nPróxima varredura em {cfg['intervalo_segundos']}s...")
            time.sleep(cfg['intervalo_segundos'])

if __name__ == "__main__":
    PoeScannerApp().run()