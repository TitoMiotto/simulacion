import random

def generar_uniforme(limite_inferior, limite_superior, tamaño_muestra):
    
    if not isinstance(limite_inferior, (int, float)):
        raise TypeError("El parámetro 'limite_inferior' debe ser un número (int o float).")
    if not isinstance(limite_superior, (int, float)):
        raise TypeError("El parámetro 'limite_superior' debe ser un número (int o float).")
    if not isinstance(tamaño_muestra, int):
        raise TypeError("El parámetro 'tamaño_muestra' debe ser un entero.")
    if limite_inferior >= limite_superior:
        raise ValueError("El valor de 'limite_inferior' debe ser menor que 'limite_superior'.")
    
    #return [random.uniform(limite_inferior, limite_superior) for _ in range(tamaño_muestra)]
    
    # Generamos la muestra de forma normal
    muestra = [random.uniform(limite_inferior, limite_superior) for _ in range(tamaño_muestra)]
    
    # Si el valor limite_superior no está en la muestra, forzamos la inclucion
    if len(muestra) == tamaño_muestra:
        if limite_superior not in muestra:
            muestra.append(limite_superior+1e-10)

    return muestra