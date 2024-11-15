import React from 'react';
import './cola.css'; // Si tienes algún estilo adicional en cola.css

const ListadoColas2 = ({ lista }) => {
  return (
    <div className="container mt-3">
      <h2>Resultado de la Simulación</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th style={{ minWidth: '100px' }}>Tiempo</th>
            <th style={{ minWidth: '120px' }}>Evento</th>
            <th style={{ minWidth: '150px' }}>Siguiente Evento</th>
            <th style={{ minWidth: '120px' }}>Vehículo</th>
            <th style={{ minWidth: '130px' }}>Tipo Vehículo</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 1</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 2</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 3</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 4</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 5</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 6</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 7</th>
            <th style={{ minWidth: '140px' }}>Estacionamiento 8</th>
            <th style={{ minWidth: '130px' }}>Recaudación</th>
            <th style={{ minWidth: '170px' }}>Estacionados esperando cobro</th>
            <th style={{ minWidth: '130px' }}>Auto cobrando</th>
            <th style={{ minWidth: '160px' }}>Prox Auto a cobrar</th>
            <th style={{ minWidth: '140px' }}>Porcentaje Uso</th>
            <th style={{ minWidth: '150px' }}>Tiempo total de espera</th>
            <th style={{ minWidth: '150px' }}>Promedio Tiempo</th>
          </tr>
        </thead>
        <tbody>
          {lista.map((item, index) => (
            <tr key={index}>
              <td>{item[0]}</td>
              <td>{item[1]}</td>
              <td>{item[2]}</td>
              <td>{item[3]}</td>
              <td>{item[4]}</td>
              <td>{item[5]}</td>
              <td>{item[6]}</td>
              <td>{item[7]}</td>
              <td>{item[8]}</td>
              <td>{item[9]}</td>
              <td>{item[10]}</td>
              <td>{item[11]}</td>
              <td>{item[12]}</td>
              <td>{item[13]}</td>
              <td>{item[14]}</td>
              <td>{item[15]}</td>
              <td>{item[16]}</td>
              <td>{item[17]}</td>
              <td>{item[18]}</td>
              <td>{item[19]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ListadoColas2;
