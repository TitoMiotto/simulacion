def calcular_histograma(data, num_intervals):
    min_val = min(data)
    max_val = max(data)
    interval_width = (max_val - min_val) / num_intervals
    intervals = []

    for i in range(num_intervals):
        primer_valor = min_val + i * interval_width
        ultimo_valor = primer_valor + interval_width
        count = len([x for x in data if primer_valor <= x < ultimo_valor])
        intervals.append({
            'primerValor': primer_valor,
            'ultimoValor': ultimo_valor,
            'cantidad': count
        })
    
    return intervals