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
    realizar_venta_mujer: float  # 1 = Uniforme, 2 = Exponencial, 3 = Normal
    encontrar_hombre: float          # Parámetro 'a' (p.ej., en uniforme, es el límite inferior)
    encontrar_mujer: float
    tabla_prob_mujer_1: float           # Parámetro 'b' (p.ej., en uniforme, es el límite superior)
    tabla_prob_mujer_2: float
    tabla_prob_mujer_3: float        # Tamaño de la muestra
    tabla_prob_hombre_1: float
    tabla_prob_hombre_2: float
    tabla_prob_hombre_3: float       # Cantidad de intervalos para el histograma
    desde: int
    hasta: int
    cantidad: int


# Ruta para generar la distribución
@app.post("/generate")
def generate_montecarlo(request: ConfiguracionRequest):
    print(f"Received request: {request}")  # Log de depuración
    try:
        
        log = []
        prob_de_vender = 0
        prob_de_vender_2mas_señora = 0
        cantidad_vendida = 0
        for count in range(0, request.cantidad):
            toco_puerta = random.random()
            abrio_puerta = False
            realizar_venta = False
            prob_cantidad = False
            vendio = 0
            if toco_puerta < 0.7:
                abrio_puerta = random.random()
                realizar_venta = random.random()
                if abrio_puerta < request.encontrar_mujer:
                    prob_de_vender+=1
                    if realizar_venta > request.realizar_venta_mujer:
                        prob_cantidad = random.random()
                        if prob_cantidad < request.tabla_prob_mujer_1:
                            vendio = 1
                        elif prob_cantidad < request.tabla_prob_mujer_2:
                            prob_de_vender_2mas_señora+=1
                            vendio = 2
                        else:
                            prob_de_vender_2mas_señora+=1
                            vendio = 3
                else:
                    if realizar_venta > 0.25:
                        prob_de_vender+=1
                        prob_cantidad = random.random()
                        if prob_cantidad < request.tabla_prob_hombre_1:
                            vendio = 1
                        elif prob_cantidad < request.tabla_prob_hombre_2:
                            vendio = 2
                        elif prob_cantidad < request.tabla_prob_hombre_3:
                            vendio = 3
                        else:
                            vendio = 4
            cantidad_vendida+=vendio
            if request.desde <= count <= request.hasta:
                nuevo_ingreso = [toco_puerta, abrio_puerta, realizar_venta, prob_cantidad, vendio, cantidad_vendida]
                log.append(nuevo_ingreso)
                print(nuevo_ingreso)

        log.append([toco_puerta, abrio_puerta, realizar_venta, prob_cantidad, vendio, cantidad_vendida])
        estadisticas = [prob_de_vender_2mas_señora/request.cantidad * 100 , prob_de_vender/request.cantidad * 100]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


    return {"data": log,
            "estadisticas": estadisticas}

# Ruta simple para verificar que el servidor está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Servidor en funcionamiento"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
