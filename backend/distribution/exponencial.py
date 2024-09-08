import random

def generar_exponencial(lambd, tamaño_muestra):
   
    if not isinstance(lambd, (int, float)):
        raise TypeError("El parámetro 'tasa' debe ser un número (int o float).")
    if not isinstance(tamaño_muestra, int):
        raise TypeError("El parámetro 'tamaño_muestra' debe ser un entero.")
    if lambd <= 0:
        raise ValueError("El valor de 'tasa' debe ser mayor que 0.")
    
    return [random.expovariate(1 / lambd) for _ in range(tamaño_muestra)]
