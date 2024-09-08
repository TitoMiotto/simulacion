import random

def generar_normal(media, desviacion_estandar, muestra):
    
    if not isinstance(media, (int, float)):
        raise TypeError("El parámetro 'media' debe ser un número (int o float).")
    if not isinstance(desviacion_estandar, (int, float)):
        raise TypeError("El parámetro 'desviacion_estandar' debe ser un número (int o float).")
    if not isinstance(muestra, int):
        raise TypeError("El parámetro 'muestra' debe ser un entero.")
    if desviacion_estandar <= 0:
        raise ValueError("El valor de 'desviacion_estandar' debe ser mayor que 0.")
    
    return [random.gauss(media, desviacion_estandar) for _ in range(muestra)]
