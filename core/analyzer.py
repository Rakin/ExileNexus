class ProfitAnalyzer:
    @staticmethod
    def scan_currencies(data, min_p, min_c, debug, divine_price, category_name):
        results = []
        if not data or 'lines' not in data:
            return results

        for item in data['lines']:
            # Extração dinâmica de nomes (Documentação oficial poe.ninja)
            name = item.get('currencyTypeName') or item.get('name')
            
            pay_data = item.get('pay', {})
            rec_data = item.get('receive', {})
            
            # Dados de liquidez (Listings)
            pay_listings = pay_data.get('listing_count', 0)
            rec_listings = rec_data.get('listing_count', 0)
            
            # Determinação do Valor de Venda (Receive) e Compra (Pay)
            # Priorizamos o valor de mercado (pay/receive), fallback para chaosValue (Scarabs/Items)
            receive_val = rec_data.get('value') or item.get('chaosValue')
            pay_val = pay_data.get('value') or item.get('chaosValue')

            if not receive_val or not pay_val:
                continue

            # Filtro de Confiança: Evitar itens "fantasmas" com poucas listagens
            is_low_confidence = (pay_listings < 2 or rec_listings < 2) if category_name != "Scarab" else False

            # Cálculo de Lucro Real (Arbitragem: Venda - Compra)
            profit_chaos = receive_val - pay_val
            profit_pct = (profit_chaos / pay_val) * 100 if pay_val > 0 else 0
            
            # Sparkline: Tendência de preço nos últimos 7 dias
            trend_data = item.get('receiveSparkLine', {}).get('totalChange', 0)

            # Classificação de Risco baseada em Tendência e Confiança
            if is_low_confidence:
                risk_level = "CRÍTICO"
            elif trend_data < -10: # Queda de mais de 10% no preço de mercado
                risk_level = "ALTO"
            else:
                risk_level = "BAIXO"

            # Filtros de Profit (Definidos no config.json)
            # Aceitamos o item se ele passar em lucro percentual OU lucro absoluto
            passou_filtro_valor = (profit_pct >= min_p or profit_chaos >= min_c)

            if passou_filtro_valor:
                # Na Dashboard, queremos ver até os de risco alto, mas marcados corretamente
                results.append({
                    'name': name,
                    'category': category_name,
                    'profit_pct': round(profit_pct, 2),
                    'profit_chaos': round(profit_chaos, 2),
                    'trend': trend_data,
                    'risk': risk_level,
                    'listings': rec_listings,
                    'buy_price': pay_val,
                    'sell_price': receive_val
                })
                    
        return results