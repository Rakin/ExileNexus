class ProfitAnalyzer:
    @staticmethod
    def scan_currencies(data, min_p, min_c, debug, divine_price):
        """
        Analisa oportunidades de lucro em moedas e fragmentos.
        Lógica: (Lucro % >= min_p) OU (Lucro Chaos >= min_c)
        """
        results = []
        if not data or 'lines' not in data:
            return results

        for item in data['lines']:
            name = item.get('currencyTypeName')
            
            # --- Dados de Mercado ---
            pay_data = item.get('pay', {})
            rec_data = item.get('receive', {})
            
            # Volume de Listagens
            pay_listings = pay_data.get('listing_count', 0)
            rec_listings = rec_data.get('listing_count', 0)
            
            receive_val = rec_data.get('value')
            pay_val = pay_data.get('value')

            # Filtro de Confiança
            is_low_confidence = (
                pay_listings == 0 and rec_listings == 0 # Só bloqueia se não houver NENHUM dado
            )

            if pay_val and receive_val:
                # Normalização do custo de compra
                real_buy_cost = 1 / pay_val if pay_val < 1.0 else pay_val
                
                profit_chaos = receive_val - real_buy_cost
                profit_pct = (profit_chaos / real_buy_cost) * 100
                
                # Tendência de preço
                trend_data = item.get('receiveSparkLine', {}).get('totalChange', 0)

                # Nível de Risco
                if is_low_confidence:
                    risk_level = "CRÍTICO"
                elif trend_data < 0 and abs(trend_data) > profit_pct:
                    risk_level = "ALTO"
                else:
                    risk_level = "BAIXO"

                if debug:
                    print(f"[DEBUG] {name:20} | Buy: {real_buy_cost:.1f} | Sell: {receive_val:.1f}")

                # --- Lógica de Filtro (PERCENTUAL OU CHAOS FIXO) ---
                passou_filtro_valor = (profit_pct >= min_p or profit_chaos >= min_c)
                
                # O bloco abaixo deve estar indentado com 4 espaços extras
                if passou_filtro_valor and not is_low_confidence:
                    results.append({
                        'name': name,
                        'buy': real_buy_cost,
                        'sell': receive_val,
                        'profit_pct': profit_pct,
                        'profit_chaos': profit_chaos,
                        'trend': trend_data,
                        'risk': risk_level,
                        'listings': rec_listings
                    })
                    
        return results