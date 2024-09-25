import React from 'react';

const ListadoMontecarlo = ({ lista }) => {
  
  return (
    <div className="container mt-3">
      <table className="table table-striped">
        <thead>
          <tr>
            <th>toco_puerta</th>
            <th>abrio_puerta</th>
            <th>realizar_venta</th>
            <th>prob_cantidad</th>
            <th>vendio</th>
            <th>cantidad_vendida</th>
          </tr>
        </thead>
        <tbody>
          {lista.map((item, index) => (
            <tr key={index}>
              <td>{item[0]}</td> {/* toco_puerta */}
              <td>{item[1]}</td> {/* abrio_puerta */}
              <td>{item[2]}</td> {/* realizar_venta */}
              <td>{item[3]}</td> {/* prob_cantidad */}
              <td>{item[4]}</td> {/* vendio */}
              <td>{item[5]}</td> {/* cantidad_vendida */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ListadoMontecarlo;
