import random

def generar_normal(media, desviacion_estandar, tamaño_muestra):
    
    if not isinstance(media, (int, float)):
        raise TypeError("El parámetro 'media' debe ser un número (int o float).")
    if not isinstance(desviacion_estandar, (int, float)):
        raise TypeError("El parámetro 'desviacion_estandar' debe ser un número (int o float).")
    if not isinstance(tamaño_muestra, int):
        raise TypeError("El parámetro 'tamaño_muestra' debe ser un entero.")
    if desviacion_estandar <= 0:
        raise ValueError("El valor de 'desviacion_estandar' debe ser mayor que 0.")
    
    #return [random.gauss(media, desviacion_estandar) for _ in range(muestra)]
    
    # Generamos la muestra de forma normal
    muestra = [random.gauss(media, desviacion_estandar) for _ in range(tamaño_muestra)]
    
    # Si el valor limite_superior no está en la muestra, forzamos la inclucion
    if len(muestra) == tamaño_muestra:
        if desviacion_estandar not in muestra:
            muestra.append(desviacion_estandar+1e-10)

    return muestra

