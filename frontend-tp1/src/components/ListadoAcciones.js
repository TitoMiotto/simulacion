import React from 'react';

const ListadoAcciones = ({ lista }) => {
  let suma = 0;
  lista.forEach(element => {
    suma += element.cantidad; // Suma total de frecuencias absolutas
  });

  let sumaAcumulada = 0;

  return (
    <div className="container mt-3">
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Intervalo</th>
            <th>Frecuencia ab</th>
            <th>Frecuencia relativa</th>
            <th>Frecuencia ab acumulada</th>
            <th>Frecuencia relativa acumulada</th>
          </tr>
        </thead>
        <tbody>
          {lista.map((intervalo, index) => {
            // Calcula la frecuencia acumulada
            sumaAcumulada += intervalo.cantidad;
            
            return (
              <tr key={index}>
                <td>{intervalo.primerValor + " - " + intervalo.ultimoValor}</td>
                <td>{intervalo.cantidad}</td>
                <td>{(intervalo.cantidad / suma).toFixed(2)}</td>
                <td>{sumaAcumulada}</td>
                <td>{(sumaAcumulada / suma).toFixed(2)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default ListadoAcciones;

