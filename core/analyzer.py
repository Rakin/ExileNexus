class ProfitAnalyzer:
    @staticmethod
    def scan_currencies(data, min_p, debug, divine_price):
        results = []
        if not data or 'lines' not in data: 
            return results

        for item in data['lines']:
            name = item.get('currencyTypeName')
            
            # --- MÉTODO 1: VOLUME DE LISTAGENS ---
            # Pegamos o número de pessoas vendendo (receive) e comprando (pay)
            pay_listings = item.get('pay', {}).get('listing_count', 0)
            rec_listings = item.get('receive', {}).get('listing_count', 0)
            
            # --- MÉTODO 2: FILTRO DE BAIXA CONFIANÇA ---
            # O Ninja usa Sparklines vazias ou flags de alerta para itens suspeitos
            # Itens estáveis têm 'data' populado na sparkline
            is_low_confidence = (
                pay_listings < 3 or 
                rec_listings < 3 or 
                item.get('lowConfidencePaySparkLine') is not None
            )

            receive_val = item.get('receive', {}).get('value')
            pay_val = item.get('pay', {}).get('value')

            if pay_val and receive_val:
                real_buy_cost = 1 / pay_val if pay_val < 1.0 else pay_val
                profit_chaos = receive_val - real_buy_cost
                profit_pct = (profit_chaos / real_buy_cost) * 100

                # Tendência para análise de risco
                trend_data = item.get('receiveSparkLine', {}).get('totalChange', 0)
                
                # Se for baixa confiança, aumentamos o risco automaticamente
                risk_level = "CRÍTICO" if is_low_confidence else ("ALTO" if trend_data < 0 and abs(trend_data) > profit_pct else "BAIXO")

                # SÓ ADICIONAR SE PASSAR NO FILTRO DE CONFIANÇA (Mínimo 5 listagens)
                if min_p <= profit_pct <= 50 and not is_low_confidence:
                    results.append({
                        'name': name,
                        'profit_pct': profit_pct,
                        'profit_chaos': profit_chaos,
                        'trend': trend_data,
                        'risk': risk_level,
                        'listings': rec_listings
                    })
        return results