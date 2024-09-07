import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import Histograma from './Histograma';
import ListadoAcciones from './ListadoAcciones';


const Acciones = () => {
  const { register, handleSubmit } = useForm();
  const [histograma, setHistograma] = useState([]);

  const onSubmit = async (data) => {
    // Puedes usar estos datos si es necesario para la solicitud
    try {
      if(data.Distribucion === "1"){
        //validaciones para la uniforme
        if(data.datoA >= data.datoB)
          throw new Error("Este es un error.");
        if(data.datoA > 0)
          throw new Error("Este es un error.");
      }else if (data.Distribucion === "2"){
        //validaciones para la exponencial
      } else{
        //validaciones para la normal
      }
      // Solicitud al backend
      const response = await axios.get('http://localhost:4000/api/Backend', {
        params: data
      });
      await setHistograma(response.data);
      // Supongamos que la respuesta contiene el histograma
      
      console.log(response.data);
      // Actualiza el estado con los datos recibidos
    } catch (error) {
      console.error(error);
    } finally{
      const histograma = [
        { primerValor: 1, ultimoValor: 50, cantidad: 10 },
        { primerValor: 51, ultimoValor: 100, cantidad: 15 },
        { primerValor: 101, ultimoValor: 123, cantidad: 50 },
        { primerValor: 124, ultimoValor: 150, cantidad: 10 },
        { primerValor: 156, ultimoValor: 180, cantidad: 10 },
        { primerValor: 181, ultimoValor: 190, cantidad: 70 },
        // más datos
      ];
      setHistograma(histograma); // Actualiza con `response.data` si es necesario
      console.log(histograma);}
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
                <option value="1">uniforme</option>
                <option value="2">exponencial</option>
                <option value="3">normal</option>
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
              <label className="mb-3">Tamaño de la muestra:</label>
              <input type="text" className="form-control" {...register('tamaño')} />
              <label className="mb-3">Cantidad de intervalos:</label>
              <input type="text" className="form-control" {...register('intervalos')} />
            </div>
            <button type="submit" className="btn btn-primary">Buscar</button>
          </form>
        </div>
      </div>
      {histograma.length > 0 && <Histograma histograma={histograma} />}
      {histograma.length > 0 && <ListadoAcciones lista={histograma} />}
    </div>
  );
};

export default Acciones;
