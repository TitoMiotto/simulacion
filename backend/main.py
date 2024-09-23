from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from distribution import calcularVisita
from distribution import probabilidades
from distribution.uniforme import generar_uniforme
from distribution.exponencial import generar_exponencial
from distribution.normal import generar_normal
from distribution.histograma import calcular_histograma
import numpy as np

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
class DistributionRequest(BaseModel):
    distribution_type: int  # 1 = Uniforme, 2 = Exponencial, 3 = Normal
    param_a: float          # Parámetro 'a' (p.ej., en uniforme, es el límite inferior)
    param_b: float          # Parámetro 'b' (p.ej., en uniforme, es el límite superior)
    sample_size: int        # Tamaño de la muestra
    intervals: int          # Cantidad de intervalos para el histograma

class RecorridoRequest(BaseModel):
    cant_N: int
    desde: int
    hasta: int
    prob_a_mujer: float
    prob_a_hombre: float
    prob_vta_m: float
    prob_cant_m1: float
    prob_cant_m2: float
    prob_cant_m3: float
    prob_cant_h1: float
    prob_cant_h2: float
    prob_cant_h3: float
    prob_cant_h4: float
    precio: float

# Ruta para generar la distribución
@app.post("/generate")
def generate_distribution(request: DistributionRequest):
    print(f"Received request: {request}")  # Log de depuración
    if request.distribution_type == 1:  # Uniforme
        try:
            result = generar_uniforme(request.param_a, request.param_b, request.sample_size)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif request.distribution_type == 2:  # Exponencial
        try:
            result = generar_exponencial(request.param_a, request.sample_size)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif request.distribution_type == 3:  # Normal
        try:
            result = generar_normal(request.param_a, request.param_b, request.sample_size)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Tipo de distribución no válida")

    print(f"Generated data: {result}")  # Log de depuración
    histograma = calcular_histograma(result, request.intervals)
    return {"data": histograma}

@app.post("/recorrido")
def recorrido(request: RecorridoRequest):
    try:
        # Extraer parámetros de la solicitud
        cant_N = request.cant_N
        desde = request.desde
        hasta = request.hasta
        
        # Validación de parámetros
        if cant_N <= 0 or desde < 0 or hasta < 0 or hasta < desde:
            raise HTTPException(status_code=400, detail="Por favor, ingrese valores válidos")

        # Cargamos las probabilidades previamente definidas
        prob = probabilidades()
        prob.prob_a_mujer = request.prob_a_mujer
        prob.prob_a_hombre = request.prob_a_hombre
        prob.prob_vta_m = request.prob_vta_m
        prob.prob_cant_m1 = request.prob_cant_m1
        prob.prob_cant_m2 = request.prob_cant_m2
        prob.prob_cant_m3 = request.prob_cant_m3
        prob.prob_cant_h1 = request.prob_cant_h1
        prob.prob_cant_h2 = request.prob_cant_h2
        prob.prob_cant_h3 = request.prob_cant_h3
        prob.prob_cant_h4 = request.prob_cant_h4
        prob.precio = request.precio

        error = prob.validar_probabilidades()
        if error:
            raise HTTPException(status_code=400, detail=error)
        
        print(f"Generated data: {prob}")  # Log de depuración

        # Inicializamos variables
        exitos = i = acu_inicial = 0
        rdos = rdo_N = []

        while i <= (cant_N - 1):
            # Generar distribución (podrías agregar más parámetros si es necesario)
            distribution_request = DistributionRequest(distribution_type=1, param_a=0, param_b=1, sample_size=cant_N)
            result = generate_distribution(distribution_request)  # Llama a la función directamente
            lista_rdo = list(calcularVisita.calcular_visita(prob))  # Supongamos que `calcular_visita` toma `prob`
            
            if lista_rdo[9] == True or lista_rdo[8] == True:
                exitos += 1
            if i >= desde and i <= hasta:
                if i == desde:
                    acu_inicial = exitos
                rdos.append(lista_rdo)
            i += 1

        return {
            "resultados": rdos,
            "exitosAcumulado": exitos,
            "ultimaVisita": False,
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Por favor, ingrese un valor numérico válido.")
        
# Ruta simple para verificar que el servidor está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Servidor en funcionamiento"}