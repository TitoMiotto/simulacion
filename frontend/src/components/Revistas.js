import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import TablaListado from './TablaListado';

// Componente principal
const Revistas = () => {
    const { register, handleSubmit } = useForm();
    const [resultados, setResultados] = useState([]);
    const [error, setError] = useState('');
    const [ultimaVisita, setUltimaVisita] = useState(null);
    const [exitosAcumulado, setExitosAcumulado] = useState('');
    const [data, setData] = useState({ limiteInferior: '', limiteSuperior: '' });

    const onSubmit = async (data) => {
        try {
            // Validaciones para los parámetros
            if (data.Filas < 1) {
                throw new Error("La cantidad de filas a generar no puede ser nula ni negativa.");
            }
            if (data.Lim_inf >= data.Lim_sup) {
                throw new Error("El limite superior del intervalo no puede ser mas chico que el limite menor.");
            }
            if (data.Lim_inf <= 0 || data.Lim_inf <= 0) {
                throw new Error("Los intervalos deben ser mayor que 0.");
            }
            if ((1 - parseFloat(data.prob_h) - parseFloat(data.prob_m)) === 0) {
                throw new Error("La distribucion de probabilidades tiene que ser 100%.");
            }
            if ((parseFloat(data.prob_h)) <= 0 || (parseFloat(data.prob_m)) <= 0) {
                throw new Error("La probabilidades no pueden ser negativas.");
            }
            if ((parseFloat(data.venta_m)) <= 0 || (parseFloat(data.venta_m)) > 1) {
                throw new Error("La probabilidad de venta debe ser un número entre 0 y 1.");
            }
            if ((parseFloat(data.venta_m)) <= 0) {
                throw new Error("La probabilidades no pueden ser negativas.");
            }
            if ((1 - parseFloat(data.subs_h_1) - parseFloat(data.subs_h_2) - parseFloat(data.subs_h_3) - parseFloat(data.subs_h_4)) === 0) {
                throw new Error("La distribucion de probabilidades tiene que ser 100%.");
            }
            if ((parseFloat(data.subs_h_1)) <= 0 || (parseFloat(data.subs_h_2)) <= 0 || (parseFloat(data.subs_h_3)) <= 0 || (parseFloat(data.subs_h_4)) <= 0) {
                throw new Error("La probabilidades no pueden ser negativas.");
            }
            if ((1 - parseFloat(data.subs_m_1) - parseFloat(data.subs_m_2) - parseFloat(data.subs_m_3)) === 0) {
                throw new Error("La distribucion de probabilidades tiene que ser 100%.");
            }
            if ((parseFloat(data.subs_m_1)) <= 0 || (parseFloat(data.subs_m_2)) <= 0 || (parseFloat(data.subs_m_3)) <= 0) {
                throw new Error("La probabilidades no pueden ser negativas.");
            }

            // Imprime los datos que se van a enviar al backend
            console.log('Datos enviados:', {
                cantidad: parseInt(data.Filas),
                desde: parseInt(data.Lim_inf),
                hasta: parseInt(data.Lim_sup),
                prob_atender_h: parseFloat(data.prob_h),
                prob_atender_m: parseFloat(data.prob_m),
                prob_venta_m: parseFloat(data.venta_m),
                prob_subs1_h: parseFloat(data.subs_h_1),
                prob_subs2_h: parseFloat(data.subs_h_2),
                prob_subs3_h: parseFloat(data.subs_h_3),
                prob_subs4_h: parseFloat(data.subs_h_4),
                prob_subs1_m: parseFloat(data.subs_m_1),
                prob_subs2_m: parseFloat(data.subs_m_3),
                prob_subs3_m: parseFloat(data.subs_m_3),
            });

            // Solicitud POST al backend con los datos validados
            const response = await axios.post('http://localhost:8000/recorrido', {
                cantidad: parseInt(data.Filas),
                desde: parseInt(data.Lim_inf),
                hasta: parseInt(data.Lim_sup),
                prob_atender_h: parseFloat(data.prob_h),
                prob_atender_m: parseFloat(data.prob_m),
                prob_venta_m: parseFloat(data.venta_m),
                prob_subs1_h: parseFloat(data.subs_h_1),
                prob_subs2_h: parseFloat(data.subs_h_2),
                prob_subs3_h: parseFloat(data.subs_h_3),
                prob_subs4_h: parseFloat(data.subs_h_4),
                prob_subs1_m: parseFloat(data.subs_m_1),
                prob_subs2_m: parseFloat(data.subs_m_3),
                prob_subs3_m: parseFloat(data.subs_m_3),
            });

            // Verifica la estructura de los datos recibidos
            if (response.data && Array.isArray(response.data.data)) {
                setUltimaVisita(response.data.data);
                setResultados(response.data.data);
                setExitosAcumulado(response.data.data);
                console.log('Response Data:', response.data.data); // Mejorado para claridad
                setError(""); // Limpiar cualquier error previo
            } else {
                throw new Error('Datos inválidos recibidos del servidor.');
            }

        } catch (error) {
            console.error('Error en la solicitud:', error.message);
            setError(error.message);  // Muestra el error al usuario
        }
    };

    return (
        <div className="container">
            <h1>Ingresar parámetros de simulación</h1>
            <hr />
            <div className="card mb-3">
                <div className="card-body">
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className="mb-3">
                            <label className="form-label">Cantidad de filas a generar:</label>
                            <input type="number" className="form-control" {...register('Filas')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Límite inferior del intervalo:</label>
                            <input type="number" className="form-control" {...register('Lim_inf')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Límite superior del intervalo:</label>
                            <input type="number" className="form-control" {...register('Lim_sup')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que atienda un hombre (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('prob_h')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que atienda una mujer (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('prob_m')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de vender a una mujer (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('venta_m')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que un hombre adquiera 1 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_h_1')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que un hombre adquiera 2 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_h_2')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que un hombre adquiera 3 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_h_3')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que un hombre adquiera 4 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_h_4')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que una mujer adquiera 1 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_m_1')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que una mujer adquiera 2 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_m_2')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Probabilidad de que una mujer adquiera 3 subcripcion (%):</label>
                            <input type="number" className="form-control" step="0.01" {...register('subs_m_3')} />
                        </div>
                        <button type="submit" className="btn btn-primary">Aceptar</button>
                    </form>
                    {error && <div className="alert alert-danger mt-3">{error}</div>} {/* Mostrar mensaje de error */}
                </div>
            </div>
            {resultados.length > 0 && (
                <TablaListado
                    resultados={resultados}
                    desde={data.Lim_inf}
                    hasta={data.Lim_sup}
                    valor={exitosAcumulado}
                    ultima={ultimaVisita}
                />
            )}
        </div>
    );
};

export default Revistas;