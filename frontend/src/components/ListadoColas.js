import React from 'react';

const ListadoColas = ({ lista }) => {

    return (
        <div className="container mt-3">
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Tiempo</th>
                        <th>Evento</th>
                        <th>Siguiente_Evento</th>
                        <th>Vehiculo</th>
                        <th>Tipo_Vehiculo</th>
                        <th>Estacionamiento 1</th>
                        <th>Estacionamiento 2</th>
                        <th>Estacionamiento 3</th>
                        <th>Estacionamiento 4</th>
                        <th>Estacionamiento 5</th>
                        <th>Estacionamiento 6</th>
                        <th>Estacionamiento 7</th>
                        <th>Estacionamiento 8</th>
                        <th>Recaudacion</th>
                        <th>Estacionados esperando cobro</th>
                        <th>Auto cobrando</th>
                        <th>prox Auto a cobrar</th>
                        <th>Porcentaje_Uso</th>
                        <th>Tiempo total de espera</th>
                        <th>Promedio_Tiempo</th>
                    </tr>
                </thead>
                <tbody>
                    {lista.map((item, index) => (
                        <tr key={index}>
                            <td>{item[0]}</td> {/* tiempo */}
                            <td>{item[1]}</td> {/* evento */}
                            <td>{item[2]}</td> {/* Proxima llegada */}
                            <td>{item[3]}</td> {/* rndTipoAuto */}
                            <td>{item[4]}</td> {/* Auto tipo */}
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

export default ListadoColas;