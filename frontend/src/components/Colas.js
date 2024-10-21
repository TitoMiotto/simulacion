import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import ListadoColas from './ListadoColas';

const Colas = () => {
    const { register, handleSubmit } = useForm();
    const [Lista, setLista] = useState([]);
    const [error, setError] = useState(""); // Estado para manejar errores
    const [estadisticas, setEstadisticas] = useState(""); // Estado para almacenar la variable de estadísticas

    const onSubmit = async (data) => {
        try {

            let dato2auto = parseFloat(data.dato1auto) + parseFloat(data.dato2auto);
            let dato2hora = parseFloat(data.dato1hora) + parseFloat(data.dato2hora);
            let dato3hora = dato2hora + parseFloat(data.dato3hora);

            // Enviar los datos al backend
            const response = await axios.post('http://localhost:8000/generate', {
                duracion_total: parseInt(data.tiempo),
                //iteraciones_mostrar: parseInt(data.iteracion_i),
                //hora_inicio: parseInt(data.hora_inicio),
                proxima_llegada: parseFloat(data.llegadas),
                tabla_prob_auto_1: parseFloat(data.dato1auto),
                tabla_prob_auto_2: parseFloat(dato2auto),
                tabla_prob_duracion1: parseFloat(data.dato1hora),
                tabla_prob_duracion2: parseFloat(dato2hora),
                tabla_prob_duracion3: parseFloat(dato3hora),
                tiempo_cobro: parseFloat(data.cobro),
            });

            // Verificar la estructura de los datos
            if (response.data && Array.isArray(response.data.data)) {
                setLista(response.data.data);
                setEstadisticas(response.data.estadisticas);
                setError(""); // Limpiar cualquier error previo
            } else {
                throw new Error('Datos inválidos recibidos del servidor.');
            }

        } catch (error) {
            console.error('Error en la solicitud:', error.message);
            setError(error.message);  // Mostrar mensaje de error al usuario
        }
    };

    return (
        <div className="container">
            <h1>Ingresar datos</h1>
            <hr />
            <div className="card mb-3">
                <div className="card-body">
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className="mb-3">
                            <label className="form-label">Tiempo de simulación:</label>
                            <input type="text" className="form-control" {...register('tiempo')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Cantidad de iteraciones a mostrar:</label>
                            <input type="text" className="form-control" {...register('iteracion_i')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Hora a partir de la cual mostrar:</label>
                            <input type="text" className="form-control" {...register('hora_inicio')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Tiempo entre llegadas:</label>
                            <input type="text" className="form-control" {...register('llegadas')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Tabla de probabilidad para tipo de vehículo:</label>
                            <input type="text" className="form-control" {...register('dato1auto')} />
                            <input type="text" className="form-control" {...register('dato2auto')} />
                            <input type="text" className="form-control" {...register('dato3auto')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Tabla de probabilidad para las horas de estacionamiento:</label>
                            <input type="text" className="form-control" {...register('dato1hora')} />
                            <input type="text" className="form-control" {...register('dato2hora')} />
                            <input type="text" className="form-control" {...register('dato3hora')} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Tiempo de cobro:</label>
                            <input type="text" className="form-control" {...register('cobro')} />
                        </div>
                        <button type="submit" className="btn btn-primary">Aceptar</button>
                    </form>
                    {error && <div className="alert alert-danger mt-3">{error}</div>} {/* Mostrar mensaje de error */}
                </div>
            </div>
            {Lista.length > 0 && (
                <>
                    <ListadoColas lista={Lista} />
                </>
            )}
            {estadisticas && (
                <div className="mt-3">
                    <h3>Estadísticas:</h3>
                    <p>{estadisticas}</p>
                </div>
            )}
        </div>
    );
};

export default Colas;