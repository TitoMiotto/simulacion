from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random

# Inicializa la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite solicitudes desde tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)
# Modelo de datos para la solicitud desde el frontend
class ConfiguracionRequest(BaseModel):
    duracion_total: int             # Tiempo simulado, parámetro solicitado al inicio...
    proxima_llegada: int            # Tiempo entre llegadas, dadas en minutos....
    tabla_prob_auto_1: float        # Probabilidad asignada a autos pequeños...
    tabla_prob_auto_2: float        # Probabilidad asignada a autos grandes...
    tabla_prob_duracion1: float     # Probabilidad en que estacione 1 hora...
    tabla_prob_duracion2: float     # Probabilidad en que estacione 2 hora...
    tabla_prob_duracion3: float     # Probabilidad en que estacione 3 hora...
    tiempo_cobro: int               # Tiempo que demora en cobrar....
    hora_inicio: int                # Tiempo en el que el log debe empezar....
    iteraciones: int                # Iteraciones a mostrar....
    

# Ruta para generar la distribución
@app.post("/generate")
def generate_colas(request: ConfiguracionRequest):
    print(f"Received request: {request}")  # Log de depuración
    try:
        # Inicialización de variables
        estacionamiento = [None] * 8        # Representa los 8 espacios de estacionamiento (None = vacío)
        salidas = []                        # Lista para almacenar salidas programadas
        zona_cobro = []                     # Lista para los vehículos en la zona de cobro
        tiempo_transcurrido = 0             # Contador del tiempo total
        log = []                            # Registro de eventos
        iteracion = 0                     # Iteraciones cortara a las 100000
        recaudacion = 0                     # Recaudacion de los cobros
        tiempo_siguiente_llegada = request.proxima_llegada  # Control de la llegada de vehículos
        tiempo_dado = request.hora_inicio   # Y aca guardamos el tiempo a partir del cual mostrar el log final
        i_a_mostrar = request.iteraciones   # Y la cantidad de iteraciones que debe tener el log final
        log_rdo = []                        # Log final a devolver
        tiempo_en_cobro = 0  # Inicializar contador de tiempo en la zona de cobro
        vehiculo_en_cobro = False           # Variable para registrar el vehículo en cobro

        # Estado inicial (tiempo 0)
        #log.append("Tiempo 0: Estacionamiento vacío.")
        log.append([0,0,"Apertura","Proxima Llegada",0,"","",0,0,0,0.0,0.0])     
        sum_tiempo_ocupado = 0
        prom_tiempo_ocupado = 0
        sum_tiempo_esperando = 0
        prom_tiempo_esperando = 0
        for tiempo_transcurrido in range(request.duracion_total):
            # Procesar entrada de vehículos
            if tiempo_transcurrido == tiempo_siguiente_llegada:  # Un vehículo llega cada proxima_llegada minutos
                #iteraciones +=1
                #iteracion += 1
                #procesar_entrada(tiempo_transcurrido)
                if None in estacionamiento:  # Hay espacio disponible
                    primer_vacio = estacionamiento.index(None)
                    
                    auto_que_entra = round(random.random(),4)
                    
                    if auto_que_entra <= request.tabla_prob_auto_1:
                        tipo_vehiculo = "Pequeño"
                    elif auto_que_entra <= (request.tabla_prob_auto_1 + request.tabla_prob_auto_2):
                        tipo_vehiculo = "Grande"
                    else:
                        tipo_vehiculo = "Utilitario"
                        
                    cuanto_dura = round(random.random(),4)
                        
                    if cuanto_dura <= request.tabla_prob_duracion1:
                        duracion_estacionamiento = 60
                    elif cuanto_dura <= (request.tabla_prob_duracion1 + request.tabla_prob_duracion2):
                        duracion_estacionamiento = 120
                    elif cuanto_dura <= (request.tabla_prob_duracion1 + request.tabla_prob_duracion2 + request.tabla_prob_duracion3):
                        duracion_estacionamiento = 180
                    else:
                        duracion_estacionamiento = 240
                    
                    # Programar salida
                    salida = tiempo_transcurrido + duracion_estacionamiento
                    salidas.append((salida, primer_vacio, tipo_vehiculo, duracion_estacionamiento))  # (minuto de salida, índice del espacio, tipo de vehículo)
                    
                    # Marcar el espacio como ocupado y almacenar el vehículo
                    estacionamiento[primer_vacio] = tipo_vehiculo
                    
                    ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                    
                    #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {tipo_vehiculo} entra en espacio {primer_vacio}. Salida programada en {salida} minutos.")
                    log.append([iteracion,tiempo_transcurrido,"Vehículo ingresa","",auto_que_entra,tipo_vehiculo,f"{primer_vacio} ocupado",cuanto_dura,duracion_estacionamiento,salida,recaudacion,prom_tiempo_ocupado,0.0])
                else:
                    #log.append([0,0,"Apertura","Proxima Llegada",0,"","",0,0,0,0.0,0.0])
                    log.append([iteracion,tiempo_transcurrido,"Estacionamiento lleno. Vehículo pasa de largo.","",0,"","",0,0,0,recaudacion,prom_tiempo_ocupado,0.0])
                    #log.append(f"Tiempo {tiempo_transcurrido}: Estacionamiento lleno. Vehículo pasa de largo.")

                tiempo_siguiente_llegada += request.proxima_llegada  # Actualizar el tiempo de la próxima llegada

            # Procesar salidas de vehículos
            """for salida in salidas[:]:  # Iterar sobre una copia de la lista
                if salida[0] <= tiempo_transcurrido:  # Si es tiempo de salida
                    #if salida[0] != tiempo_transcurrido: iteracion+=1
                    if len(zona_cobro) < 2:  # Si hay espacio en la zona de cobro
                        if salida[2] == "Pequeño":
                            recaudacion += round(salida[3] * round((500/60),4),0)
                        elif salida[2] == "Grande":
                            recaudacion += round(salida[3] * round((1500/60),4),0)
                        else:
                            recaudacion += round(salida[3] * round((3000/60),4),0)
                        sum_tiempo_ocupado+=salida[3]
                        prom_tiempo_ocupado= round(sum_tiempo_ocupado/(tiempo_transcurrido*8),4)
                        zona_cobro.append(salida)  # Mover a la zona de cobro
                        salidas.remove(salida)  # Eliminar de la lista de salidas
                        #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {salida[2]} en espacio {salida[1]} va a la zona de cobro.")
                        #ocupados = sum(1 for espacio in estacionamiento if espacio is not None) -1
                        #log.append([iteraciones,tiempo_transcurrido,"Vehículo va a la zona de cobro","",0,salida[2],f"{salida[1]}",0,0,0,recaudacion,(ocupados/8),0.0])
                    else:
                        ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                        print("*"*60)
                        tiempo_hasta_esperar = zona_cobro[0][0] + request.tiempo_cobro
                        sum_tiempo_esperando+= tiempo_hasta_esperar - tiempo_transcurrido
                        log.append([iteracion,tiempo_transcurrido,"Vehículo no puede ir a cobro, espera","",0,salida[2],f"{salida[1]}",0,0,0,recaudacion,prom_tiempo_ocupado,0.0])
                        #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo en espacio {salida[1]} no puede ir a cobro, espera.")"""
            
            # Lista para llevar un control de los vehículos en espera
            vehiculos_espera = []

            # Procesar salidas de vehículos
            for salida in salidas[:]:  # Iterar sobre una copia de la lista
                if salida[0] <= tiempo_transcurrido:  # Si es tiempo de salida
                    # Verificamos si hay espacio en la zona de cobro
                    if len(zona_cobro) < 2:
                        # Calcular el cobro según el tipo de vehículo
                        if salida[2] == "Pequeño":
                            recaudacion += round(salida[3] * round((500 / 60), 4), 0)
                        elif salida[2] == "Grande":
                            recaudacion += round(salida[3] * round((1500 / 60), 4), 0)
                        else:
                            recaudacion += round(salida[3] * round((3000 / 60), 4), 0)

                        # Actualizar tiempos de ocupación y estadísticas
                        sum_tiempo_ocupado += salida[3]
                        prom_tiempo_ocupado = round(sum_tiempo_ocupado / (tiempo_transcurrido * 8), 4)

                        # Mover a la zona de cobro y registrar el evento en el log
                        zona_cobro.append(salida)  # Mover a la zona de cobro
                        salidas.remove(salida)  # Eliminar de la lista de salidas

                        # Eliminar de la lista de espera si estaba esperando
                        if salida in vehiculos_espera:
                            vehiculos_espera.remove(salida)
                        
                        # Registro de cobro en el log
                        log.append([
                            iteracion,
                            tiempo_transcurrido,
                            f"Vehículo en zona de cobro y se libera espacio {salida[1]}",
                            "", 0,
                            salida[2] + " Cobrando",
                            f"{salida[1]} Libre",
                            0, 0, 0,
                            recaudacion,
                            (sum(1 for espacio in estacionamiento if espacio is not None) / 8),
                            prom_tiempo_ocupado
                        ])
                    
                    else:
                        # Si la zona de cobro está llena, el vehículo debe esperar
                        if salida not in vehiculos_espera:
                            vehiculos_espera.append(salida)  # Añadir a la lista de espera
                            
                            # Registrar solo una vez el mensaje de espera en el log
                            log.append([
                                iteracion,
                                tiempo_transcurrido,
                                "Vehículo en espera",
                                "", 0,
                                "Esperando",
                                "Sin espacio",
                                0, 0, 0,
                                recaudacion,
                                (sum(1 for espacio in estacionamiento if espacio is not None) / 8),
                                prom_tiempo_ocupado
                            ])

                # Manejo de cobro de vehículos en la zona de cobro
                # Incrementar el tiempo en cobro para los vehículos que están en la zona de cobro
                for vehiculo in zona_cobro:
                    tiempo_en_cobro += 1  # Aumentar el tiempo en cobro

                # Verificar si el tiempo en cobro ha alcanzado el tiempo requerido
                if tiempo_en_cobro >= request.tiempo_cobro:
                    vehiculo_cobro = zona_cobro[0]  # Obtener el vehículo en cobro
                    espacio_libre = vehiculo_cobro[1]  # Suponiendo que el índice 1 es el espacio del vehículo en la zona de cobro
                    
                    # Marcar el espacio como libre
                    estacionamiento[espacio_libre] = None  # Liberar el espacio en el estacionamiento
                    zona_cobro.pop(0)  # Remover el vehículo que ha sido cobrado
                    tiempo_en_cobro = 0  # Reiniciar el contador de tiempo en cobro

                    # Registrar salida del vehículo
                    log.append([
                        iteracion,
                        tiempo_transcurrido + request.tiempo_cobro,
                        "Vehículo se retira",
                        "", 0,
                        vehiculo_cobro[2] + " se Retira",
                        f"{espacio_libre} Libre",
                        0, 0, 0,
                        recaudacion,
                        (sum(1 for espacio in estacionamiento if espacio is not None) / 8),
                        prom_tiempo_ocupado
                    ])

                    # Manejo de la lista de vehículos en espera si la zona de cobro se queda con menos de 2 vehículos
                    if len(zona_cobro) < 2 and vehiculos_espera:
                        # Mover el siguiente vehículo de la lista de espera a la zona de cobro
                        siguiente_vehiculo = vehiculos_espera.pop(0)  # Obtener el primer vehículo en espera
                        zona_cobro.append(siguiente_vehiculo)  # Moverlo a la zona de cobro
                        salidas.remove(siguiente_vehiculo)  # Eliminar de la lista de salidas

                        # Registro de cobro en el log para el nuevo vehículo
                        log.append([
                            iteracion,
                            tiempo_transcurrido,
                            f"Vehículo {siguiente_vehiculo[1]} entra a zona de cobro",
                            "", 0,
                            siguiente_vehiculo[2] + " Cobrando",
                            f"{siguiente_vehiculo[1]} en cobro",
                            0, 0, 0,
                            recaudacion,
                            (sum(1 for espacio in estacionamiento if espacio is not None) / 8),
                            prom_tiempo_ocupado
                        ])
            # Procesar cobro de vehículos en la zona de cobro
            """if zona_cobro:
                
                # Procesar el vehículo que llegó primero
                vehiculo_cobro = zona_cobro[0]
                ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                
                if zona_cobro[0] != tiempo_transcurrido: iteracion+=1

                #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {vehiculo_cobro[2]} en zona de cobro se está cobrando.")
                
                # Liberar el espacio en el estacionamiento
                espacio_libre = vehiculo_cobro[1]  # Obtener el espacio que se va a liberar
                estacionamiento[espacio_libre] = None  # Marcar el espacio como libre
                zona_cobro.pop(0)  # Remover el vehículo que ha sido cobrado
                #log.append(f"Tiempo {tiempo_transcurrido}: Espacio {espacio_libre} liberado.")
                log.append([iteracion,tiempo_transcurrido,f"Vehículo en zona de cobro y se libera espacio {espacio_libre}","",0,vehiculo_cobro[2]+" Cobrando",f"{espacio_libre} Libre",0,0,0,recaudacion,(ocupados/8),0.0])
                
                tiempo_transcurrido += request.tiempo_cobro  # Tiempo de cobro
                
                iteracion+=1

                #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {vehiculo_cobro[2]} salió de la zona de cobro.")
                log.append([iteracion,tiempo_transcurrido,f"Vehículo se retira","",0,vehiculo_cobro[2]+" se Retira",f"{espacio_libre} Libre",0,0,0,recaudacion,(ocupados/8),0.0])"""
            
            """if zona_cobro:
                
                # Procesar el vehículo que llegó primero
                vehiculo_cobro = zona_cobro[0]
                ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                
                if zona_cobro[0] != tiempo_transcurrido: iteracion+=1
                
                # Incrementa el tiempo en cobro en lugar de `tiempo_transcurrido`
                tiempo_en_cobro += 1
                
                # Liberar el espacio en el estacionamiento
                espacio_libre = vehiculo_cobro[1]  # Obtener el espacio que se va a liberar
                estacionamiento[espacio_libre] = None  # Marcar el espacio como libre
                
                # Registrar el evento en log
                log.append([iteracion,tiempo_transcurrido,f"Vehículo en zona de cobro y se libera espacio {espacio_libre}","",0,vehiculo_cobro[2]+" Cobrando",f"{espacio_libre} Libre",0,0,0,recaudacion,prom_tiempo_ocupado,0.0])


                # Cuando el tiempo en cobro alcanza `request.tiempo_cobro`, se completa el cobro
                if tiempo_en_cobro >= request.tiempo_cobro:
                    
                    zona_cobro.pop(0)  # Remover el vehículo que ha sido cobrado
                    
                    tiempo_en_cobro = 0  # Reiniciar el contador de tiempo en cobro                    
                    
                    iteracion += 1  # Incremento de la iteración
                    log.append([iteracion, tiempo_transcurrido + request.tiempo_cobro, f"Vehículo se retira", "", 0, vehiculo_cobro[2] + " se Retira", f"{espacio_libre} Libre", 0, 0, 0, recaudacion, prom_tiempo_ocupado, 0.0])"""
            
            # En la sección donde procesas cobros en la zona de cobro, realiza este cambio
            """ if zona_cobro:
                vehiculo_cobro = zona_cobro[0]
                ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                
                # Incrementa el tiempo en cobro en lugar de `tiempo_transcurrido`
                tiempo_en_cobro += 1
                
                #if zona_cobro[0] == tiempo_transcurrido: iteracion-=1
                
                if vehiculo_en_cobro:
                    
                    # Liberar el espacio en el estacionamiento
                    espacio_libre = vehiculo_cobro[1]
                                        
                    # Registrar el evento en log
                    log.append([iteracion, tiempo_transcurrido, f"Vehículo en zona de cobro y se libera espacio {espacio_libre}", "", 0, vehiculo_cobro[2] + " Cobrando", f"{espacio_libre} Libre", 0, 0, 0, recaudacion, (ocupados / 8), 0.0])
                    
                    vehiculo_en_cobro = True
                    #iteracion += 1

                # Cuando el tiempo en cobro alcanza `request.tiempo_cobro`, se completa el cobro
                if tiempo_en_cobro >= request.tiempo_cobro:
                    estacionamiento[espacio_libre] = None
                    zona_cobro.pop(0)  # Remover el vehículo que ha sido cobrado
                    tiempo_en_cobro = 0  # Reiniciar el contador de tiempo en cobro
                    
                    #iteracion += 1  # Incremento de la iteración
                    vehiculo_en_cobro = False                   
                    # Registrar salida del vehículo
                    log.append([iteracion, tiempo_transcurrido + request.tiempo_cobro, f"Vehículo se retira", "", 0, vehiculo_cobro[2] + " se Retira", f"{espacio_libre} Libre", 0, 0, 0, recaudacion, (ocupados / 8), 0.0])"""

            if iteracion > 10000:
                ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                log.append([iteracion,tiempo_transcurrido,"Finalizacion por Iteracin N° 10000","",0,"","",0,0,0,0.0,0.0])
                #log.append(f"Tiempo {tiempo_transcurrido} finalizacion por llegar al maximo.")
                break

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    log_ordenado = sorted(log, key=lambda x: x[1])
    
    # Recorremos hasta el penúltimo elemento para evitar index out of range
    for i in range(1,len(log_ordenado) - 1):
        # Asigna el "Evento Actual" de la siguiente fila al espacio vacío de la fila actual
        log_ordenado[i][3] = log_ordenado[i + 1][2]  
        
    log_unico = []

    for i in range(1, len(log_ordenado)):
        fila_actual = log_ordenado[i]
        fila_previa = log_ordenado[i - 1]
        
        # Compara el tiempo en la columna 2 (índice 1)
        if fila_actual[1] != fila_previa[1]:  # Si el tiempo es diferente
            log_unico.append([iteracion] + fila_actual[1:])  # Añade el contador y el resto de la fila
            iteracion += 1  # Incrementa el contador
        else:
            log_unico.append([iteracion - 1] + fila_actual[1:])  # Mantiene el mismo contador
    
    # Imprimir el log de eventos completo
    for evento in log_unico:
        print(evento)
        
    return {"data": log_unico}
    #return {"data": log_rdo}

# Ruta simple para verificar que el servidor está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Servidor en funcionamiento"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
