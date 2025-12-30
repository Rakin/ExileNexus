import os, time, json, winsound
from core.api import PoeNinjaAPI
from core.analyzer import ProfitAnalyzer

class PoeScannerApp:
    def load_config(self):
        with open('config.json', 'r') as f: return json.load(f)

    def run(self):
        while True:
            cfg = self.load_config()
            os.system('cls' if os.name == 'nt' else 'clear')
            api = PoeNinjaAPI(cfg['league'])
            
            # Passo 1: Pegar o preço do Divine atualizado
            divine_price = api.get_divine_price()
            
            print(f"--- POE SCANNER PRO ---")
            print(f"Liga: {cfg['league']} | 1 Divine = {divine_price:.1f} Chaos\n")
            
            # Passo 2: Buscar dados de Currency/Fragment
            data = api.get_currency_data("Currency")
            ops = ProfitAnalyzer.scan_currencies(data, cfg['min_profit_percent'], cfg['debug'], divine_price)

            if ops:
                print(f"--- Oportunidades Encontradas ---")
                for op in ops:
                    print(f"[PROFIT] {op['name']:20} | {op['profit_pct']:.2f}%")
                    print(f"        Lucro: {op['profit_div']:.4f} Divines ({op['profit_div'] * divine_price:.1f}c)")
                    if op['profit_pct'] >= 5: winsound.Beep(1000, 200)
            
            time.sleep(cfg['intervalo_segundos'])

if __name__ == "__main__":
    PoeScannerApp().run()