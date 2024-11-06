from random import random


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
        print(self.tiempoLlegada)
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
    
    def quitarVehiculo(self):
        self.utilizacion += self.TiempoEstacionado
        V = self.Vehiculo
        self.Vehiculo = None
        self.randomTiempo = 0
        return V
    
    def utilizacionReal(self, tiempo):
        return self.utilizacion + (tiempo - self.Vehiculo.tiempoLlegada)

    @classmethod
    def setTablaValores(cls, valor1, valor2, valor3):
        cls.tabla_valor1 = valor1
        cls.tabla_valor2 = valor2
        cls.tabla_valor3 = valor3

"""Auto2 = Vehiculo(0.34, 320)
Auto1 = Vehiculo(0.31, 22)
#print(Auto2.tipo)

E1 = Estacionamiento()
E1.setVehiculo(Auto2, 0.45)
#print(E1.TiempoEstacionado,E1.vehiculo.tipo)"""


class LlegadaVehiculo:
    vector_estacionamientos = None

    tiempoEntreLlegadas = 0

    def __init__(self, tiempo):
        self.tiempo = tiempo
        self.rndTipo = 0
        self.tipo = ""

    def simular(self):
        for i in range(7):
            if self.__class__.vector_estacionamientos[i].Vehiculo is None:
                self.rndTipo = random()
                v1 = Vehiculo(self.rndTipo, self.tiempo)
                self.tipo = v1.getTipo()
                self.__class__.vector_estacionamientos[i].setVehiculo(v1, random())
                return [FinDeEstacionamiento(self.tiempo + self.__class__.vector_estacionamientos[i].TiempoEstacionado, i), LlegadaVehiculo(self.tiempo + self.__class__.tiempoEntreLlegadas)]
        print("vehiculo se retira")
        return [LlegadaVehiculo(self.tiempo + self.__class__.tiempoEntreLlegadas)]  # Retornar lista vacía si no se cumplen las condiciones

    def print(self):
        return "Llegada de vehiculo tiempo: " + str(self.tiempo) + ", proxima llegada: " + str(self.tiempoEntreLlegadas + self.tiempo) + " Rnd Tipo de auto " + str(self.rndTipo) + " tipo: " + self.tipo

     
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
            return [self.__class__.sectorCobro.setProximo(self.vector_estacionamientos[self.indiceEstacionamiento].quitarVehiculo())]
        
    def print(self):
        return "Fin de estacionamiento tiempo: " + str(self.tiempo) + ", estacionamiento: " + str(self.indiceEstacionamiento)



class SectorCobro:
    vector_estacionamientos = None
    def __init__(self, tiempoCobro):
        self.tiempoCobro = tiempoCobro
        self.vector_espera = []
        self.sum_cobro = 0
        self.contadorEstacionamientos = 0
        self.proximo = None
        self.Actual = None
        self.totalMinEsperados = 0

    def setProximo(self, Vehiculo):
        if self.Actual:
            self.proximo = Vehiculo
            return -1
        else:
            self.Actual = Vehiculo
            return EventoCobro(Vehiculo.tiempoLlegada + Vehiculo.tiempoEstacionado + self.tiempoCobro)

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
                self.totalMinEsperados += tiempo - (estacionamiento1.TiempoEstacionado + estacionamiento1.Vehiculo.tiempoLlegada)
                self.proximo = estacionamiento1.quitarVehiculo()
            else:
                self.proximo = None
            return True
        self.Actual = None

        return False
                


class EventoCobro:
    sectorCobro = None

    def __init__(self, tiempo):
        self.tiempo = tiempo

    def simular(self):
        self.__class__.sectorCobro.contadorEstacionamientos += 1
        self.__class__.sectorCobro.sum_cobro+= (self.__class__.sectorCobro.Actual.tiempoEstacionado/60) * self.__class__.sectorCobro.Actual.tipo * 500 

        if self.__class__.sectorCobro.buscarSiguiente(self.tiempo):
            return [EventoCobro(self.tiempo + self.sectorCobro.tiempoCobro)]
        return []

    def print(self):
        return "Cobro " + "tiempo" + str(self.tiempo) 

vector_estacionamientos = [Estacionamiento(), Estacionamiento(), Estacionamiento(),Estacionamiento(), Estacionamiento(), Estacionamiento(),Estacionamiento(), Estacionamiento()]
"""L = LlegadaVehiculo(1)
ll = LlegadaVehiculo(25)
L.simular()
print(ll.simular())
print(LlegadaVehiculo.vector_estacionamientos[1].TiempoEstacionado)
print(LlegadaVehiculo.vector_estacionamientos[1].Vehiculo.tipo)
print(LlegadaVehiculo.vector_estacionamientos[1].Vehiculo.tiempoLlegada)"""

sectorCobro = SectorCobro(7)
SectorCobro.vector_estacionamientos = vector_estacionamientos
Vehiculo.setTablaValores(0.1,0.5,1)    
Estacionamiento.setTablaValores(0.15, 0.34, 0.67)
LlegadaVehiculo.vector_estacionamientos = vector_estacionamientos
LlegadaVehiculo.tiempoEntreLlegadas = 13
FinDeEstacionamiento.sectorCobro = sectorCobro
FinDeEstacionamiento.vector_estacionamientos = vector_estacionamientos
EventoCobro.sectorCobro = sectorCobro
vector_eventos = [LlegadaVehiculo(1)]
i = 0

while i < len(vector_eventos):
    utilizacionTotal = 0
    # Imprimir el evento actual en la lista
    nuevos = [evento for evento in vector_eventos[i].simular() if evento != -1]
    print("Procesando evento:", vector_eventos[i].print())
    # Estado de los estacionamientos
    print("\n--- Estado de Estacionamientos ---")

    for idx, estacionamiento in enumerate(vector_estacionamientos):
        
        if estacionamiento.Vehiculo:
            print(f"Estacionamiento {idx + 1}: Vehiculo tipo {estacionamiento.Vehiculo.tipo}, Tiempo Llegada {estacionamiento.Vehiculo.tiempoLlegada},  Rnd de tiempo {estacionamiento.randomTiempo}, Tiempo Estacionado {estacionamiento.TiempoEstacionado}, Hora de irse {estacionamiento.TiempoEstacionado + estacionamiento.Vehiculo.tiempoLlegada}, El tiempo utilizado es {estacionamiento.utilizacionReal(vector_eventos[i].tiempo)}")
            utilizacionTotal += estacionamiento.utilizacionReal(vector_eventos[i].tiempo)
        else:
            print(f"Estacionamiento {idx + 1}: Vacío")
    print(f"La utilizacion de estacionamiento {utilizacionTotal/(8*vector_eventos[i].tiempo)}: ")
    
    # Estado del Sector de Cobro
    print("\n--- Estado del Sector Cobro ---")
    if sectorCobro.Actual:
        print(f"Vehículo Actual en Cobro: Tipo {sectorCobro.Actual.tipo}, Tiempo Llegada {sectorCobro.Actual.tiempoLlegada}, Tiempo Estacionado {sectorCobro.Actual.tiempoEstacionado}")
    else:
        print("Vehículo Actual en Cobro: Ninguno")
    
    if sectorCobro.proximo:
        print(f"Vehículo en Espera para Cobro: Tipo {sectorCobro.proximo.tipo}, Tiempo Llegada {sectorCobro.proximo.tiempoLlegada}, Tiempo Estacionado {sectorCobro.proximo.tiempoEstacionado}")
    else:
        print("Vehículo en Espera para Cobro: Ninguno")
    
    print(f"Total Cobro Acumulado: {sectorCobro.sum_cobro}")
    print(f"Contador de Estacionamientos Finalizados: {sectorCobro.contadorEstacionamientos}")
    print(f"Vehículos en Espera para Cobro: {len(sectorCobro.vector_espera)}")
    print(f"El total de minutos de espera es: {sectorCobro.totalMinEsperados}")
    
    # Procesar el evento actual y agregar nuevos eventos según el resultado

    # Añadir los nuevos eventos al vector_eventos
    for nuevo in nuevos:
        vector_eventos.append(nuevo)
    
    # Ordenar los eventos por tiempo
    vector_eventos.sort(key=lambda x: x.tiempo)
    
    i += 1  # Avanzar al siguiente evento
    if i >100: break
    
    print("\n--- Fin de la Iteración ---\n")


