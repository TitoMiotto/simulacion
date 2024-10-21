import React from 'react';

const ListadoColas = ({ lista }) => {

    return (
        <div className="container mt-3">
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Iteracion</th>
                        <th>Tiempo</th>
                        <th>Evento</th>
                        <th>Siguiente_Evento</th>
                        <th>Vehiculo</th>
                        <th>Tipo_Vehiculo</th>
                        <th>Estacionamiento</th>
                        <th>Duracion</th>
                        <th>Tipo_Salida</th>
                        <th>Salida</th>
                        <th>Recaudacion</th>
                        <th>Porcentaje_Uso</th>
                        <th>Promedio_Tiempo</th>
                    </tr>
                </thead>
                <tbody>
                    {lista.map((item, index) => (
                        <tr key={index}>
                            <td>{item[0]}</td> {/* Iteracion */}
                            <td>{item[1]}</td> {/* Tiempo */}
                            <td>{item[2]}</td> {/* Evento */}
                            <td>{item[3]}</td> {/* Siguiente_Evento */}
                            <td>{item[4]}</td> {/* Vehiculo */}
                            <td>{item[5]}</td> {/* Tipo_Vehiculo */}
                            <td>{item[6]}</td> {/* Estacionamiento */}
                            <td>{item[7]}</td> {/* Duracion */}
                            <td>{item[8]}</td> {/* Tipo_Salida */}
                            <td>{item[9]}</td> {/* Salida */}
                            <td>{item[10]}</td> {/* Recaudacion */}
                            <td>{item[11]}</td> {/* Porcentaje_Uso */}
                            <td>{item[12]}</td> {/* Promedio_Tiempo */}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ListadoColas;