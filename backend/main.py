from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from distribution.uniforme import generar_uniforme
from distribution.exponencial import generar_exponencial
from distribution.normal import generar_normal

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
    return {"data": result}

# Ruta simple para verificar que el servidor está en funcionamiento
@app.get("/")
def read_root():
    return {"message": "Servidor en funcionamiento"}
