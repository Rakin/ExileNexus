class ProfitAnalyzer:
    @staticmethod
    def scan_currencies(data, min_p, debug, divine_price):
        results = []
        if not data or 'lines' not in data: return results

        for item in data['lines']:
            name = item.get('currencyTypeName')
            receive = item.get('receive', {}).get('value')
            pay = item.get('pay', {}).get('value')

            if pay and receive:
                # Normalização para a economia do Standard (Inversão de Pay)
                real_buy_cost = 1 / pay if pay < 1.0 else pay
                
                profit_chaos = receive - real_buy_cost
                profit_pct = (profit_chaos / real_buy_cost) * 100

                # CONVERSÃO CHAOS => DIVINE
                profit_divine = profit_chaos / divine_price

                if debug:
                    print(f"[DEBUG] {name:20} | Buy: {real_buy_cost:.1f}c | Sell: {receive:.1f}c | {profit_pct:.2f}%")

                if min_p <= profit_pct <= 50:
                    results.append({
                        'name': name,
                        'buy': real_buy_cost,
                        'sell': receive,
                        'profit_pct': profit_pct,
                        'profit_div': profit_divine
                    })
        return results