import React from 'react';

const ListadoMontecarlo = ({ lista }) => {

  return (
    <div className="container mt-3">
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Visita</th>
            <th>Toco_Puerta</th>
            <th>Atendieron?</th>
            <th>Abrio_Puerta</th>
            <th>Quien?</th>
            <th>Realizar_Venta</th>
            <th>Vendieron?</th>
            <th>Prob_Cantidad</th>
            <th>Vendio</th>
            <th>Cantidad_Vendida</th>
            <th>Venta_Mujer</th>
            <th>Venta_2_Mujer</th>
            <th>Comision_Ganada</th>
          </tr>
        </thead>
        <tbody>
          {lista.map((item, index) => (
            <tr key={index}>
              <td>{item[10]}</td> {/* Visita */}
              <td>{item[0]}</td> {/* Toco_Puerta */}
              <td>{item[8]}</td> {/* Atendieron? */}
              <td>{item[1]}</td> {/* Abrio_Puerta */}
              <td>{item[7]}</td> {/* Quien? */}
              <td>{item[2]}</td> {/* Realizar_Venta */}
              <td>{item[9]}</td> {/* Vendieron? */}
              <td>{item[3]}</td> {/* Prob_Cantidad */}
              <td>{item[4]}</td> {/* Vendio */}
              <td>{item[5]}</td> {/* Cantidad_Vendida */}
              <td>{item[11]}</td> {/* Venta_Mujer */}
              <td>{item[12]}</td> {/* Venta_2_Mujer */}
              <td>{item[6]}</td> {/* Comision_Ganada */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ListadoMontecarlo;
