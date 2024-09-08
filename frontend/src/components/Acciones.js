import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import Histograma from './Histograma';
import ListadoAcciones from './ListadoAcciones';

const Acciones = () => {
  const { register, handleSubmit } = useForm();
  const [histograma, setHistograma] = useState([]);
  const [error, setError] = useState(""); // Estado para manejar errores

  const onSubmit = async (data) => {
    try {
      // Validaciones para la distribución uniforme
      if (data.Distribucion === "1") {
        if (parseFloat(data.datoA) >= parseFloat(data.datoB)) {
          throw new Error("Dato A debe ser menor que Dato B para la distribución uniforme.");
        }
        if (parseFloat(data.datoA) <= 0) {
          throw new Error("Dato A debe ser mayor que 0 para la distribución uniforme.");
        }
      }
      // Validaciones para la distribución exponencial
      else if (data.Distribucion === "2") {
        if (parseFloat(data.datoA) <= 0) {
          throw new Error("Dato A debe ser mayor que 0 para la distribución exponencial.");
        }
      }
      // Validaciones para la distribución normal
      else if (data.Distribucion === "3") {
        if (parseFloat(data.datoA) <= 0 || parseFloat(data.datoB) <= 0) {
          throw new Error("Tanto Dato A (media) como Dato B (desviación estándar) deben ser mayores que 0 para la distribución normal.");
        }
      }
  
      // Imprime los datos que se van a enviar al backend
      console.log('Datos enviados:', {
        distribution_type: parseInt(data.Distribucion),
        param_a: parseFloat(data.datoA),
        param_b: parseFloat(data.datoB),
        sample_size: parseInt(data.tamaño),
        intervals: parseInt(data.intervalos)
      });
  
      // Solicitud POST al backend
      const response = await axios.post('http://localhost:8000/generate', {
        distribution_type: parseInt(data.Distribucion),
        param_a: parseFloat(data.datoA),
        param_b: parseFloat(data.datoB),
        sample_size: parseInt(data.tamaño),
        intervals: parseInt(data.intervalos)
      });
  
      // Verifica la estructura de los datos recibidos
      if (response.data && Array.isArray(response.data.data)) {
        setHistograma(response.data.data);
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
      <h1>Ingresar datos</h1>
      <hr />
      <div className="card mb-3">
        <div className="card-body">
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className="mb-3">
              <label className="form-label">Distribución:</label>
              <select className="form-select" {...register('Distribucion')}>
                <option value="1">Uniforme</option>
                <option value="2">Exponencial</option>
                <option value="3">Normal</option>
              </select>
            </div>
            <div className="mb-3">
              <label className="form-label">Dato A:</label>
              <input type="text" className="form-control" {...register('datoA')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Dato B:</label>
              <input type="text" className="form-control" {...register('datoB')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Tamaño de la muestra:</label>
              <input type="text" className="form-control" {...register('tamaño')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Cantidad de intervalos:</label>
              <input type="text" className="form-control" {...register('intervalos')} />
            </div>
            <button type="submit" className="btn btn-primary">Buscar</button>
          </form>
          {error && <div className="alert alert-danger mt-3">{error}</div>} {/* Mostrar mensaje de error */}
        </div>
      </div>
      {histograma.length > 0 && <Histograma histograma={histograma} />}
      {histograma.length > 0 && <ListadoAcciones lista={histograma} />}
    </div>
  );
};

export default Acciones;
