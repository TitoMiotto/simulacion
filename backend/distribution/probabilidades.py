class probabilidades:
    def __init__(self):
        # Inicializamos las variables de la clase...
        self.prob_a_mujer = None
        self.prob_a_hombre = None
        self.prob_vta_m = None
        self.prob_cant_m1 = None
        self.prob_cant_m2 = None
        self.prob_cant_m3 = None
        self.prob_cant_h1 = None
        self.prob_cant_h2 = None
        self.prob_cant_h3 = None
        self.prob_cant_h4 = None
        self.precio = None

    def validar_probabilidades(self):
        try:
            # Verificamos que los valores no sean negativos.....
            if self.prob_a_mujer is None or self.prob_a_hombre is None or self.prob_vta_m is None \
                    or self.prob_cant_m1 is None or self.prob_cant_m2 is None or self.prob_cant_m3 is None \
                    or self.prob_cant_h1 is None or self.prob_cant_h2 is None or self.prob_cant_h3 is None \
                    or self.prob_cant_h4 is None or self.precio is None:
                raise ValueError("Debe asignar valores a todas las probabilidades y al precio.")
            if self.prob_a_mujer < 0 or self.prob_a_hombre < 0 or self.prob_vta_m < 0 \
                    or self.prob_cant_m1 < 0 or self.prob_cant_m2 < 0 or self.prob_cant_m3 < 0 \
                    or self.prob_cant_h1 < 0 or self.prob_cant_h2 < 0 or self.prob_cant_h3 < 0 or self.prob_cant_h4 < 0 \
                    or self.precio < 0:
                raise ValueError("Las probabilidades y el precio no pueden ser negativos.")   
            
            # Verificamos que las probabilidades esten bien distribuidas.....          
            if round(self.prob_a_mujer + self.prob_a_hombre, 5) != 1:
                raise ValueError("La suma de las probabilidades de atención debe ser igual a 1.")
            if round((self.prob_cant_m1 + self.prob_cant_m2 + self.prob_cant_m3), 5) != 1:
                raise ValueError("La suma de las probabilidades de venta para mujeres debe ser igual a 1.")
            if round((self.prob_cant_h1 + self.prob_cant_h2 + self.prob_cant_h3 + self.prob_cant_h4), 5) != 1:
                raise ValueError("La suma de las probabilidades de venta para hombres debe ser igual a 1.")
        except ValueError as e:
            return str(e)

    def obtener_probabilidades(self):
        # Devolvemos el diccionario con los elementos....
        probabilidad = {
            "atencion": {
                "nadie": 0.3,
                "atiende_m": {
                    "prob_m": self.prob_a_mujer,
                    "vende_m": self.prob_vta_m,
                    "prob_subs_m": {
                        "subs_1": self.prob_cant_m1,
                        "subs_2": self.prob_cant_m2,
                        "subs_3": self.prob_cant_m3
                    }
                },
                "atiende_h": {
                    "prob_h": self.prob_a_hombre,
                    "vende_h": 0.25,
                    "prob_subs_h": {
                        "subs_1": self.prob_cant_h1,
                        "subs_2": self.prob_cant_h2,
                        "subs_3": self.prob_cant_h3,
                        "subs_4": self.prob_cant_h4
                    }
                }
            },
            "g_por_vta": self.precio
        }
        return probabilidad
