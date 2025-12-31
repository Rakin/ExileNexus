class ProfitAnalyzer:
    @staticmethod
    def scan_currencies(data, min_p, min_c, debug, divine_price, category_name):
        results = []
        if not data or 'lines' not in data:
            return results

        for item in data['lines']:
            name = item.get('currencyTypeName') or item.get('name') # Suporte para Scarabs/Items
            
            pay_data = item.get('pay', {})
            rec_data = item.get('receive', {})
            
            pay_listings = pay_data.get('listing_count', 0)
            rec_listings = rec_data.get('listing_count', 0)
            
            # Para Scarabs, usamos chaosValue se o receive['value'] não existir
            receive_val = rec_data.get('value') or item.get('chaosValue')
            pay_val = pay_data.get('value')

            # Filtro de Confiança: Pelo menos 2 listagens (ou ignorar se for Scarab que não tem contagem clara)
            is_low_confidence = (pay_listings < 2 and rec_listings < 2) if pay_val else False

            if receive_val:
                # Se for Moeda/Fragmento (tem pay_val), calcula custo real. 
                # Se for Scarab, o custo de compra é o próprio chaosValue do Ninja.
                if pay_val:
                    real_buy_cost = 1 / pay_val if pay_val < 1.0 else pay_val
                else:
                    real_buy_cost = receive_val # Arbitragem de Scarab exige dados externos, mantemos paridade aqui

                profit_chaos = receive_val - real_buy_cost
                profit_pct = (profit_chaos / real_buy_cost) * 100 if real_buy_cost > 0 else 0
                
                trend_data = item.get('receiveSparkLine', {}).get('totalChange', 0)

                # Nível de Risco
                if is_low_confidence:
                    risk_level = "CRÍTICO"
                elif trend_data < 0 and abs(trend_data) > profit_pct:
                    risk_level = "ALTO"
                else:
                    risk_level = "BAIXO"

                # --- DEFINIÇÃO DA VARIÁVEL QUE FALTOU ---
                passou_filtro_valor = (profit_pct >= min_p or profit_chaos >= min_c)

                if passou_filtro_valor and not is_low_confidence:
                    results.append({
                        'name': name,
                        'category': category_name,
                        'profit_pct': profit_pct,
                        'profit_chaos': profit_chaos,
                        'trend': trend_data,
                        'risk': risk_level,
                        'listings': rec_listings
                    })
                    
        return results