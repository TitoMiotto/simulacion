import random

class calcularVisita:
    def __init__(self):
        # Inicializamos valores de clase...
        self.rnd_1 = None
        self.rnd_2 = None
        self.rnd_3 = None
        self.rnd_4 = None
        self.flag_atend_m = False
        self.flag_atend_h = False
        self.flag_venta_m = False
        self.flag_venta_h = False
        self.subscripciones = 0
        self.ganancia = 0

    def calcular_visita(self, prob):
        self.rnd_1 = random.random()

        # Aca chequeamos primero que nada si lo atienden, probabilidad fija de 0,3.....
        if self.rnd_1 > prob["atencion"]["nadie"]:
            self.rnd_2 = random.random()

            # Luego hacemos una verificacion de quien lo atendio, empezamos con la mujer
            # y si no se cumple deducimos que fue el hombre.....
            if self.rnd_2 <= prob["atencion"]["atiende_m"]["prob_m"]:
                self.flag_atend_m = True
                self.rnd_3 = random.random()

                # Aca vemos si se logra vender la subcripcion o no....
                if self.rnd_3 <= prob["atencion"]["atiende_m"]["vende_m"]:
                    self.rnd_4 = random.random()

                    # Y aca calculamos cuantas subscripciones puede llegar a comprar la mujer...
                    self.subscripciones = self.prob_subs(prob["atencion"]["atiende_m"]["prob_subs_m"], self.rnd_4)
                    
                    # Y por ultimo dejamos marcado que se vendio a una mujer...
                    self.flag_venta_m = True
            else:
                self.flag_atend_h = True
                self.rnd_3 = random.random()

                # Aca vemos si se logra vender la subcripcion o no....
                if self.rnd_3 <= prob["atencion"]["atiende_h"]["vende_h"]:
                    self.rnd_4 = random.random()

                    # Y aca calculamos cuantas subscripciones puede llegar a comprar el hombre...
                    self.subscripciones = self.prob_subs(prob["atencion"]["atiende_m"]["prob_subs_m"], self.rnd_4)
                    # Y por ultimo dejamos marcado que se vendio a un hombre...
                    self.flag_venta_h = True

        # Antes de terminar hacemos un calculo rapido de cuanto gano por las subscripciones... nulo si no vendio nada...
        self.ganancia = self.subscripciones * prob["g_por_vta"]

        # Aca retornaremos los valores de las variables y flags para armar el string de info de la visita
        # Basicamente se podran interpretar sabiendo si estan en 0.0 y false o no... para interpretar dichos rdos....
        return self.rnd_1, self.rnd_2, self.rnd_3, self.rnd_4, self.subscripciones, self.ganancia, self.flag_atend_m, self.flag_atend_h, self.flag_venta_m, self.flag_venta_h

    def prob_subs(self, probabilidades, rnd):
        # Inicializamos variables de control y acumulacion...
        subs = 0
        prob_acu = 0.0

        # Recorremos el diccionario provisto previamente ordenado y vamos chequeando con las probabilidades acumuladas...
        # Sabiendo que el maximo de opciones es 4 no importa que entre una de 3... porque son las mismos valores en ambas...
        for x in dict(sorted(probabilidades.items(), key=lambda x: x[1])):
            prob_acu += probabilidades[x]
            if rnd <= prob_acu:
                subs = int(x.split('_')[-1])  # Usar 'subs' como separador
                break
        return subs