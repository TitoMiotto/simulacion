from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from random import random

# Inicializa la aplicación FastAPI
app = FastAPI()


class Vehiculo:
    tabla_valor1 = 10
    tabla_valor2 = 20
    tabla_valor3 = 30

    def __init__(self, randomTipo, tiempoLlegada):
        self.randomTipo = randomTipo
        self.tiempoLlegada = tiempoLlegada
        self.tiempoEstacionado = 0
        if randomTipo < self.__class__.tabla_valor1:
            self.tipo = 1
        elif randomTipo < self.__class__.tabla_valor2:
            self.tipo = 3
        elif randomTipo < self.__class__.tabla_valor3:
            self.tipo = 6
        else:
            self.tipo = None  # Manejo en caso de que no se cumpla ninguna condición

    def getTiempoLlegada(self):
        return self.tiempoLlegada
    
    def setTiempoEstacionado(self, tiempo):
        self.tiempoEstacionado = tiempo

    def getTipo(self):
        if self.tipo < 2: return "Pequeño"
        if self.tipo < 4: return "Grande"
        if self.tipo < 7: return "Utilitario"
    
    @classmethod
    def setTablaValores(cls, valor1, valor2, valor3):
        cls.tabla_valor1 = valor1
        cls.tabla_valor2 = valor2
        cls.tabla_valor3 = valor3

class Estacionamiento:

    tabla_valor1 = 0,1
    tabla_valor2 = 0,20
    tabla_valor3 = 0,70

    def __init__(self):
        self.Vehiculo = None
        self.randomTiempo = 0
        self.tiempo = 0
        self.utilizacion = 0
    
    def setVehiculo(self, Vehiculo, randomTiempo):
        self.Vehiculo = Vehiculo
        self.randomTiempo = randomTiempo
        if randomTiempo < self.__class__.tabla_valor1:
            self.TiempoEstacionado = 60
        elif randomTiempo < self.__class__.tabla_valor2:
            self.TiempoEstacionado = 120
        elif randomTiempo < self.__class__.tabla_valor3:
            self.TiempoEstacionado = 180
        else:
            self.TiempoEstacionado = 240  # Manejo en caso de que no se cumpla ninguna condición
        Vehiculo.setTiempoEstacionado(self.TiempoEstacionado)
    
    def quitarVehiculo(self, tiempoExtra):
        self.utilizacion += tiempoExtra + self.TiempoEstacionado
        V = self.Vehiculo
        self.Vehiculo = None
        self.randomTiempo = 0
        return V
    
    def utilizacionActual(self, tiempo):
        if self.Vehiculo:
            return self.utilizacion + (tiempo - self.Vehiculo.tiempoLlegada)
        return self.utilizacion

    @classmethod
    def setTablaValores(cls, valor1, valor2, valor3):
        cls.tabla_valor1 = valor1
        cls.tabla_valor2 = valor2
        cls.tabla_valor3 = valor3


class LlegadaVehiculo:
    vector_estacionamientos = None
    tiempoEntreLlegadas = 0

    def __init__(self, tiempo):
        self.tiempo = tiempo
        self.rndTipo = 0
        self.tipo = ""

    def simular(self):
        for i in range(8):
            if self.__class__.vector_estacionamientos[i].Vehiculo is None:
                self.rndTipo = random()
                v1 = Vehiculo(self.rndTipo, self.tiempo)
                self.tipo = v1.getTipo()
                self.__class__.vector_estacionamientos[i].setVehiculo(v1, random())
                return [FinDeEstacionamiento(self.tiempo + self.__class__.vector_estacionamientos[i].TiempoEstacionado, i), LlegadaVehiculo(self.tiempo + self.__class__.tiempoEntreLlegadas)]

        return [LlegadaVehiculo(self.tiempo + self.__class__.tiempoEntreLlegadas)]  # Retornar lista vacía si no se cumplen las condiciones

    def print(self):

        return (str(self.tiempo), str(self.tiempoEntreLlegadas + self.tiempo), str(self.rndTipo), self.tipo)
    
    def getEvento(self):
        return "Llegada de vehiculo"

    def getTiempo(self):
        return self.tiempo


class FinDeEstacionamiento:
    vector_estacionamientos = None
    sectorCobro = None

    def __init__(self, tiempo, indiceEstacionamiento):
        self.tiempo = tiempo
        self.indiceEstacionamiento = indiceEstacionamiento

    def simular(self):
        if not self.__class__.sectorCobro.AceptaVehiculo():
            self.__class__.sectorCobro.vector_espera.append(self.indiceEstacionamiento)
            return [-1]
        else:
            return [self.__class__.sectorCobro.setProximo(self.vector_estacionamientos[self.indiceEstacionamiento].quitarVehiculo(0), self.tiempo)]
        
    def print(self):
        return (str(self.tiempo), str(self.indiceEstacionamiento))

    def getEvento(self):
        return f"Fin de Estacionamiento cochera{self.indiceEstacionamiento + 1}"

    def getTiempo(self):
        return self.tiempo

class SectorCobro:
    vector_estacionamientos = None
    def __init__(self, tiempoCobro):
        self.tiempoCobro = tiempoCobro
        self.vector_espera = []
        self.vector_calculo_demoras = []
        self.sum_cobro = 0
        self.contadorEstacionamientos = 0
        self.proximo = None
        self.Actual = None
        self.totalMinEsperados = 0

    def setProximo(self, Vehiculo, tiempo):
        if self.Actual:
            self.proximo = Vehiculo
            return -1
        else:
            self.Actual = Vehiculo
            t = self.calcularDemoraCobrado(tiempo)
            return EventoCobro(tiempo + t)

    def AceptaVehiculo(self):
        if not self.proximo or not self.Actual:
            return True
        return False
    
    def buscarSiguiente(self, tiempo):
        if self.proximo:

            self.Actual = self.proximo
            if self.vector_espera:
                indice = self.vector_espera.pop(0)
                estacionamiento1 = self.__class__.vector_estacionamientos[indice]
                tiempoExtraEsperado = tiempo - (estacionamiento1.TiempoEstacionado + estacionamiento1.Vehiculo.tiempoLlegada)
                self.totalMinEsperados += tiempoExtraEsperado
                self.contadorEstacionamientos +=1
                self.proximo = estacionamiento1.quitarVehiculo(tiempoExtraEsperado)
            else:
                self.proximo = None
            return True
        self.Actual = None

        return False
    
    def printEstacionamientos(self, tiempo):
        mensaje=[""] * 8
        for idx, estacionamiento in enumerate(self.vector_estacionamientos):
            if estacionamiento.Vehiculo:
                mensaje[idx]=(f"Estacionamiento {idx + 1}: \nVehiculo tipo {estacionamiento.Vehiculo.tipo}, \nTiempo Llegada {estacionamiento.Vehiculo.tiempoLlegada},  \nRnd de tiempo {estacionamiento.randomTiempo}, \nTiempo Estacionado {estacionamiento.TiempoEstacionado}, \nHora de irse {estacionamiento.TiempoEstacionado + estacionamiento.Vehiculo.getTiempoLlegada()}")

            else:
                mensaje[idx] = "vacio"
            mensaje[idx] += (f"\nTiempo Utilizado {estacionamiento.utilizacionActual(tiempo)}")
        return mensaje
    
    def promMin(self):
        if self.contadorEstacionamientos:
            prom = self.totalMinEsperados/self.contadorEstacionamientos
        else:
            prom = 0
        return prom
    
    def getProximo(self):
        if self.proximo != None:
            return f"Vehiculo que llego en {self.proximo.tiempoLlegada}"
        else:
            return "Vacio"
        
    def getActual(self):
        if self.Actual != None:
            return f"Vehiculo que llego en {self.Actual.tiempoLlegada}"
        else:
            return "Vacio"
        
    def UtilizacionTotalActual(self,tiempo):
        sum = 0
        if tiempo == 0:
            return 0
        
        for i in self.vector_estacionamientos:
            sum += i.utilizacionActual(tiempo)
        return sum/(8*tiempo)

    def cobrar(self):
        self.sum_cobro += (self.Actual.tiempoEstacionado/60) * self.Actual.tipo * 500

    def calcularDemoraCobrado(self, tiempo):
        if not self.AceptaVehiculo():
            C = len(self.vector_espera) + 1
        elif self.proximo:
            C = 1
        elif self.Actual:
            C = 0
        
        
        D = 130
        t = DActual = 0 
        derivada = 0
        if self.Actual.tipo == 3:
            D = 180
        tabla = [self.Actual.getTipo(), D, C,tiempo]
        while DActual < D:
            log = []
            log.append(t)
            log.append(DActual)
            derivada = C + 0.2*self.tiempoCobro+t*t
            log.append(derivada)
            t += 1
            DActual +=  derivada
            log.append(t)
            log.append(DActual)
            tabla.append(log)
        self.vector_calculo_demoras.append(tabla)
        print(tabla)
        return t

        



class EventoCobro:
    sectorCobro = None

    def __init__(self, tiempo):
        self.tiempo = tiempo

    def simular(self):
        self.__class__.sectorCobro.cobrar()
        
        if self.__class__.sectorCobro.buscarSiguiente(self.tiempo):
            t = self.__class__.sectorCobro.calcularDemoraCobrado(self.tiempo)
            return [EventoCobro(self.tiempo + t)]
        return []

    def print(self):
        return str(self.tiempo) 
    
    def getEvento(self):
        return "Cobrar a Auto"
    
    def getTiempo(self):
        return self.tiempo

  
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
    tiempo_cobro: float               # Tiempo que demora en cobrar....
    hora_inicio: int                # Tiempo en el que el log debe empezar....
    iteraciones: int                # Iteraciones a mostrar....
    

# Ruta para generar la distribución
@app.post("/generate")
def generate_colas(request: ConfiguracionRequest):
    print(f"Received request: {request}")  # Log de depuración
    try:
        vector_estacionamientos = [Estacionamiento(), Estacionamiento(), Estacionamiento(),Estacionamiento(), Estacionamiento(), Estacionamiento(),Estacionamiento(), Estacionamiento()]
        sectorCobro = SectorCobro(request.tiempo_cobro)
        SectorCobro.vector_estacionamientos = vector_estacionamientos
        LlegadaVehiculo.vector_estacionamientos = vector_estacionamientos
        FinDeEstacionamiento.vector_estacionamientos = vector_estacionamientos
        Vehiculo.setTablaValores(request.tabla_prob_auto_1,request.tabla_prob_auto_2,1)    
        Estacionamiento.setTablaValores(request.tabla_prob_duracion1, request.tabla_prob_duracion2, request.tabla_prob_duracion3)
        LlegadaVehiculo.tiempoEntreLlegadas = request.proxima_llegada
        FinDeEstacionamiento.sectorCobro = sectorCobro
        EventoCobro.sectorCobro = sectorCobro
        vector_eventos = [LlegadaVehiculo(request.proxima_llegada)]
        # Crear una lista para almacenar los datos de cada iteración
        i = 0
        registro_iteraciones = []
        while vector_eventos[i].tiempo < request.duracion_total:

            # Imprimir el evento actual en la lista
            nuevos = [evento for evento in vector_eventos[i].simular() if evento != -1]
            ProxLlegada = RndTipoAuto = AutoTipo = 0
            # Estado de los estacionamientos
            if isinstance(vector_eventos[i],LlegadaVehiculo):

                tiempo, ProxLlegada, RndTipoAuto, AutoTipo = vector_eventos[i].print()

            
            evento = vector_eventos[i].getEvento()
            tiempo = vector_eventos[i].getTiempo()

            
            mensaje = sectorCobro.printEstacionamientos(tiempo)
            actual = sectorCobro.getActual()
            proximo = sectorCobro.getProximo()
            promTotalMinEsperados = sectorCobro.promMin()
            colaEspera = len(sectorCobro.vector_espera)
            utilizacionTotal = sectorCobro.UtilizacionTotalActual(tiempo)

            registro_iteraciones.append([
                        tiempo, evento, ProxLlegada, RndTipoAuto, AutoTipo,
                        mensaje[0],mensaje[1],mensaje[2],mensaje[3],mensaje[4], \
                        mensaje[5],mensaje[6],mensaje[7], \
                        sectorCobro.sum_cobro, colaEspera, actual, proximo,\
                        utilizacionTotal, sectorCobro.totalMinEsperados, promTotalMinEsperados
                    ])
            # Añadir los nuevos eventos al vector_eventos
            for nuevo in nuevos:
                vector_eventos.append(nuevo)
            
            # Ordenar los eventos por tiempo
            vector_eventos.sort(key=lambda x: x.tiempo)
            
            i += 1  # Avanzar al siguiente evento


                    
        return {"data": registro_iteraciones,
                "tablas": sectorCobro.vector_calculo_demoras}
        #return {"data": log_rdo}
    except Exception as e:
    # Maneja cualquier otra excepción y accede al error con 'e'
     print(f"Ocurrió un error: {e}")

# Ruta simple para verificar que el servidor está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Servidor en funcionamiento"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
