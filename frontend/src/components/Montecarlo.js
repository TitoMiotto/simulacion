import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import ListadoMontecarlo from './ListadoMontecarlo';

const MonteCarlo = () => {
  const { register, handleSubmit } = useForm();
  const [Lista, setLista] = useState([]);
  const [error, setError] = useState(""); // Estado para manejar errores
  const [estadisticas, setEstadisticas] = useState(""); // Estado para almacenar la variable


  const onSubmit = async (data) => {
    try {
      // Validaciones para la distribución uniforme
      if (parseInt(data.precio) < 0){
        throw new Error("El valor de la comision del vendedor no puede ser negativa.")
      }
      if (parseFloat(data.datoA) < 0 || parseFloat(data.datoA) > 1) {
        throw new Error("Este valor debe estar entre 0 y 1.");
      }
      // Validaciones para la distribución exponencial
      if ((parseFloat(data.datoB) + parseFloat(data.datoC)) !== 1) {
        throw new Error("La suma de las probabilidades de encontrar a la señora y señor de la casa deben ser igual a 1.");
      }
      if (parseFloat(data.datoB) <0 || parseFloat(data.datoC) <0 || parseFloat(data.datoB) > 1 || parseFloat(data.datoC) > 1) {
        throw new Error("La suma de las probabilidades de encontrar a la señora y señor de la casa deben estar entre 0 y 1.");
      }
      // 
      if (Math.round(((parseFloat(data.dato1mujer) + parseFloat(data.dato2mujer) + parseFloat(data.dato3mujer)) * 1000) / 1000) !== 1) {
        throw new Error("La suma de las probabilidades de la tabla de la señora deben ser igual a 1.");
      }       
      if (parseFloat(data.dato1mujer) < 0 || parseFloat(data.dato2mujer) <0 || parseFloat(data.dato3mujer)<0 || parseFloat(data.dato1mujer) > 1 || parseFloat(data.dato2mujer) > 1 || parseFloat(data.dato3mujer) > 1 ) {
        throw new Error("La suma de las probabilidades de la tabla de la señora deben estar entre 0 y 1.");
      }
      if (parseFloat(data.dato1hombre) + parseFloat(data.dato2hombre) + parseFloat(data.dato3hombre) + parseFloat(data.dato4hombre) !== 1) {
        throw new Error("La suma de las probabilidades de la tabla del señor deben ser igual a 1.");
      }
      if (parseFloat(data.dato1hombre) < 0 || parseFloat(data.dato2hombre) < 0 || parseFloat(data.dato3hombre) < 0 || parseFloat(data.dato4hombre) < 0 || parseFloat(data.dato1hombre) > 1 || parseFloat(data.dato2hombre) > 1 || parseFloat(data.dato3hombre) > 1 || parseFloat(data.dato4hombre) > 1 ) {
        throw new Error("La suma de las probabilidades de la tabla del señor deben estar entre 0 y 1.");
      }
      if (parseFloat(data.desde) >= parseFloat(data.hasta) || parseFloat(data.desde) < 0 || parseFloat(data.hasta) > parseFloat(data.tamaño)) {
        throw new Error("Los parametros para mostrar la tabla estan incorrectos.");
      }
      // Imprime los datos que se van a enviar al backend

      let dato2hombre = parseFloat(data.dato1hombre) + parseFloat(data.dato2hombre);
      let dato3hombre = dato2hombre + parseFloat(data.dato3hombre);
      let dato2mujer = parseFloat(data.dato1mujer) + parseFloat(data.dato2mujer);
      let dato3mujer = dato2mujer + parseFloat(data.dato3mujer);
      let dato4hombre = dato3hombre + parseFloat(data.dato4hombre);
      console.log('Datos enviados:', {
        realizar_venta_mujer: parseFloat(data.datoA),
        encontrar_mujer: parseFloat(data.datoB),
        encontrar_hombre: parseFloat(data.datoC),
        tabla_prob_mujer_1: parseFloat(data.dato1mujer),
        tabla_prob_mujer_2: parseFloat(dato2mujer),
        tabla_prob_mujer_3: parseFloat(dato3mujer),
        tabla_prob_hombre_1: parseFloat(data.dato1hombre),
        tabla_prob_hombre_2: parseFloat(dato2hombre),
        tabla_prob_hombre_3: parseFloat(dato3hombre),
        tabla_prob_hombre_4: parseFloat(dato4hombre),
        desde: parseInt(data.desde),
        hasta: parseInt(data.hasta),
        cantidad: parseInt(data.tamaño),
        comision: parseInt(data.precio)
      });


      // Solicitud POST al backend
      const response = await axios.post('http://localhost:8000/generate', {
        realizar_venta_mujer: parseFloat(data.datoA),
        encontrar_mujer: parseFloat(data.datoB),
        encontrar_hombre: parseFloat(data.datoC),
        tabla_prob_mujer_1: parseFloat(data.dato1mujer),
        tabla_prob_mujer_2: parseFloat(data.dato2mujer),
        tabla_prob_mujer_3: parseFloat(data.dato3mujer),
        tabla_prob_hombre_1: parseFloat(data.dato1hombre),
        tabla_prob_hombre_2: parseFloat(data.dato2hombre),
        tabla_prob_hombre_3: parseFloat(data.dato3hombre),
        desde: parseInt(data.desde),
        hasta: parseInt(data.hasta),
        cantidad: parseInt(data.tamaño),
        comision: parseInt(data.precio)
      });

      // Verifica la estructura de los datos recibidos
      if (response.data && Array.isArray(response.data.data)) {
        setLista(response.data.data);
        console.log('Response Data:', response.data.data); // Mejorado para claridad
        setEstadisticas(response.data.estadisticas);
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
              <label className="form-label">Realizar venta a la señora de la casa:</label>
              <input type="text" className="form-control" {...register('datoA')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Encontrar a la señora de la casa:</label>
              <input type="text" className="form-control" {...register('datoB')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Encontrar al señor de la casa:</label>
              <input type="text" className="form-control" {...register('datoC')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Tabla de prob. para la señora:</label>
              <input type="text" className="form-control" {...register('dato1mujer')} />
              <input type="text" className="form-control" {...register('dato2mujer')} />
              <input type="text" className="form-control" {...register('dato3mujer')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Tabla de prob. para el señor:</label>
              <input type="text" className="form-control" {...register('dato1hombre')} />
              <input type="text" className="form-control" {...register('dato2hombre')} />
              <input type="text" className="form-control" {...register('dato3hombre')} />
              <input type="text" className="form-control" {...register('dato4hombre')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Mostrar desde-hasta:</label>
              <input type="text" className="form-control" {...register('desde')} />
              <input type="text" className="form-control" {...register('hasta')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Tamaño de la muestra:</label>
              <input type="text" className="form-control" {...register('tamaño')} />
            </div>
            <div className="mb-3">
              <label className="form-label">Comision del vendedor:</label>
              <input type="text" className="form-control" {...register('precio')} />
            </div>
            <button type="submit" className="btn btn-primary">Aceptar</button>
          </form>
          {error && <div className="alert alert-danger mt-3">{error}</div>} {/* Mostrar mensaje de error */}
        </div>
        <div className="mt-3">
          <label>La probabilidad de vender 2 o mas a una señora es:</label>
          <div>{estadisticas[0]}</div> {/* Muestra el valor */}
        </div>
        <div className="mt-3">
          <label>La probabilidad de vender del vendedor es:</label>
          <div>{estadisticas[1]}</div> {/* Muestra el valor */}
        </div>
      </div>
      {Lista.length > 0 && (
        <>
          {console.log(Lista)} {/* Depuración para verificar los datos */}
          <ListadoMontecarlo lista={Lista} />
        </>
      )}

    </div>
  );
};

export default MonteCarlo;
