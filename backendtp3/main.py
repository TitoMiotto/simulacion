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

# Ruta para generar la distribución
@app.post("/generate")
def generate_colas(request: ConfiguracionRequest):
    print(f"Received request: {request}")  # Log de depuración
    try:
        # Inicialización de variables
        estacionamiento = [None] * 8    # Representa los 8 espacios de estacionamiento (None = vacío)
        salidas = []                    # Lista para almacenar salidas programadas
        zona_cobro = []                 # Lista para los vehículos en la zona de cobro
        tiempo_transcurrido = 0         # Contador del tiempo total
        log = []                        # Registro de eventos
        iteraciones = 0                 # Iteraciones cortara a las 100000
        recaudacion = 0                 # Recaudacion de los cobros
        tiempo_cobrado = 0              # Cuanto tiempo se gasto en cobros 
        tiempo_siguiente_llegada = request.proxima_llegada  # Control de la llegada de vehículos
        
        # Estado inicial (tiempo 0)
        #log.append("Tiempo 0: Estacionamiento vacío.")
        log.append([0,0,"Apertura","Proxima Llegada",0,"","",0,0,0,0.0,0.0])     
           
        for tiempo_transcurrido in range(request.duracion_total):
            # Procesar entrada de vehículos
            if tiempo_transcurrido == tiempo_siguiente_llegada:  # Un vehículo llega cada proxima_llegada minutos
                iteraciones +=1
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
                    salidas.append((salida, primer_vacio, tipo_vehiculo))  # (minuto de salida, índice del espacio, tipo de vehículo)
                    
                    # Marcar el espacio como ocupado y almacenar el vehículo
                    estacionamiento[primer_vacio] = tipo_vehiculo
                    
                    ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                    
                    #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {tipo_vehiculo} entra en espacio {primer_vacio}. Salida programada en {salida} minutos.")
                    log.append([iteraciones,tiempo_transcurrido,"Vehículo ingresa","",auto_que_entra,tipo_vehiculo,f"{primer_vacio} ocupado",cuanto_dura,duracion_estacionamiento,salida,recaudacion,(ocupados/8),0.0])
                else:
#                            log.append([0,0,"Apertura","Proxima Llegada",0,"","",0,0,0,0.0,0.0])
                    log.append([iteraciones,tiempo_transcurrido,"Estacionamiento lleno. Vehículo pasa de largo.","",0,"","",0,0,0,recaudacion,1.0,0.0])
                    #log.append(f"Tiempo {tiempo_transcurrido}: Estacionamiento lleno. Vehículo pasa de largo.")

                tiempo_siguiente_llegada += request.proxima_llegada  # Actualizar el tiempo de la próxima llegada

            # Procesar salidas de vehículos
            for salida in salidas[:]:  # Iterar sobre una copia de la lista
                if salida[0] <= tiempo_transcurrido:  # Si es tiempo de salida
                    if len(zona_cobro) < 2:  # Si hay espacio en la zona de cobro
                        if salida[2] == "Pequeño":
                            recaudacion += salida[0] * round((500/60),4)
                        elif salida[2] == "Grande":
                            recaudacion += salida[0] * round((1500/60),4)
                        else:
                            recaudacion += salida[0] * round((3000/60),4)

                        zona_cobro.append(salida)  # Mover a la zona de cobro
                        salidas.remove(salida)  # Eliminar de la lista de salidas
                        #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {salida[2]} en espacio {salida[1]} va a la zona de cobro.")
                        #ocupados = sum(1 for espacio in estacionamiento if espacio is not None) -1
                        #log.append([iteraciones,tiempo_transcurrido,"Vehículo va a la zona de cobro","",0,salida[2],f"{salida[1]}",0,0,0,recaudacion,(ocupados/8),0.0])
                    else:
                        ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                        log.append([iteraciones,tiempo_transcurrido,"Vehículo no puede ir a cobro, espera","",0,salida[2],f"{salida[1]}",0,0,0,recaudacion,(ocupados/8),0.0])
                        #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo en espacio {salida[1]} no puede ir a cobro, espera.")

            # Procesar cobro de vehículos en la zona de cobro
            if zona_cobro:
                # Procesar el vehículo que llegó primero
                vehiculo_cobro = zona_cobro[0]
                ocupados = sum(1 for espacio in estacionamiento if espacio is not None)

                #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {vehiculo_cobro[2]} en zona de cobro se está cobrando.")
                
                # Liberar el espacio en el estacionamiento
                espacio_libre = vehiculo_cobro[1]  # Obtener el espacio que se va a liberar
                estacionamiento[espacio_libre] = None  # Marcar el espacio como libre
                zona_cobro.pop(0)  # Remover el vehículo que ha sido cobrado
                #log.append(f"Tiempo {tiempo_transcurrido}: Espacio {espacio_libre} liberado.")
                log.append([iteraciones,tiempo_transcurrido,f"Vehículo en zona de cobro y se libera espacio {espacio_libre}","",0,vehiculo_cobro[2]+" Cobrando",f"{espacio_libre} Libre",0,0,0,recaudacion,(ocupados/8),0.0])

                iteraciones +=1

                tiempo_transcurrido += request.tiempo_cobro  # Tiempo de cobro
                #log.append(f"Tiempo {tiempo_transcurrido}: Vehículo {vehiculo_cobro[2]} salió de la zona de cobro.")
                log.append([iteraciones,tiempo_transcurrido,f"Vehículo se retira","",0,vehiculo_cobro[2]+" se Retira",f"{espacio_libre} Libre",0,0,0,recaudacion,(ocupados/8),0.0])


            if iteraciones > 10000:
                ocupados = sum(1 for espacio in estacionamiento if espacio is not None)
                log.append([iteraciones,tiempo_transcurrido,"Finalizacion por Iteracin N° 10000","",0,"","",0,0,0,0.0,0.0])
                #log.append(f"Tiempo {tiempo_transcurrido} finalizacion por llegar al maximo.")
                break

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Imprimir el log de eventos
    for evento in log:
        print(evento)

    return {"data": log}

# Ruta simple para verificar que el servidor está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Servidor en funcionamiento"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
