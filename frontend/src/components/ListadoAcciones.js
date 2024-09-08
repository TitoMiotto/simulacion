import React from 'react';

const ListadoAcciones = ({ lista }) => {
  let suma = 0;
  let sumaAcumulada = 0;

  // Verifica si `lista` es un array
  if (!Array.isArray(lista)) {
    console.error('La lista no es un array:', lista);
    return <p>Error: Los datos no están en formato de lista.</p>;
  }

  // Calcula la suma total de frecuencias absolutas
  lista.forEach(element => {
    if (typeof element.cantidad === 'number') {
      suma += element.cantidad;
    } else {
      console.error('Cantidad no es un número:', element.cantidad);
    }
  });

  // Verifica si la suma es válida
  if (suma === 0) {
    console.warn('La suma total de frecuencias es 0');
  }

  return (
    <div className="container mt-3">
      <h2>Listado de Acciones</h2>
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
            const cantidad = typeof intervalo.cantidad === 'number' ? intervalo.cantidad : 0;
            sumaAcumulada += cantidad;

            const primerValor = typeof intervalo.primerValor === 'number' ? intervalo.primerValor : 0;
            const ultimoValor = typeof intervalo.ultimoValor === 'number' ? intervalo.ultimoValor : 0;

            return (
              <tr key={index}>
                <td>{`${primerValor} - ${ultimoValor}`}</td>
                <td>{cantidad}</td>
                <td>{suma > 0 ? (cantidad / suma).toFixed(2) : '0.00'}</td>
                <td>{sumaAcumulada}</td>
                <td>{suma > 0 ? (sumaAcumulada / suma).toFixed(2) : '0.00'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default ListadoAcciones;
