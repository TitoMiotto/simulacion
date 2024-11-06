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
                        <th>Cola de espera Cobro en estacionamiento</th>
                        <th>Auto cobrando</th>
                        <th>prox Auto a cobrar</th>
                        <th>Porcentaje_Uso</th>
                        <th>Tiempo total de espera</th>
                        <th>Promedio_Tiempo</th>
                    </tr>
                </thead>
                ([
                        tiempo, evento, ProxLlegada, RndTipoAuto, AutoTipo,
                        mensaje[0],mensaje[1],mensaje[2],mensaje[3],mensaje[4], \
                        mensaje[5],mensaje[6],mensaje[7], \
                        sectorCobro.sum_cobro, sectorCobro.vector_espera, sectorCobro.Actual.getTiempoLlegada, sectorCobro.proximo.getTiempoLlegada,\
                        (utilizacionTotal/(8*vector_eventos[i].tiempo)), sectorCobro.totalMinEsperados, sectorCobro.totalMinEsperados/sectorCobro.contadorEstacionamientos
                    ])
                <tbody>
                    {lista.map((item, index) => (
                        <tr key={index}>
                            <td>{item[0]}</td> {/* tiempo */}
                            <td>{item[1]}</td> {/* evento */}
                            <td>{item[2]}</td> {/* Proxima llegada */}
                            <td>{item[3]}</td> {/* rndTipoAuto */}
                            <td>{item[4]}</td> {/* Auto tipo */}
                            <td>{item[5]}</td> {/* estacionamiento0 */}
                            <td>{item[6]}</td> {/* estacionamiento */}
                            <td>{item[7]}</td> {/* estacionamiento */}
                            <td>{item[8]}</td> {/* estacionamiento */}
                            <td>{item[9]}</td> {/* estacionamiento */}
                            <td>{item[10]}</td> {/* estacionamiento */}
                            <td>{item[11]}</td> {/* estacionamiento */}
                            <td>{item[12]}</td> {/* estacionamiento */}
                            <td>{item[13]}</td> {/* estacionamiento */}
                            <td>{item[14]}</td> {/* estacionamiento */}
                            <td>{item[15]}</td> {/* estacionamiento */}
                            <td>{item[16]}</td> {/* estacionamiento */}
                            <td>{item[17]}</td> {/* estacionamiento */}
                            <td>{item[18]}</td> {/* estacionamiento */}
                            <td>{item[19]}</td> {/* estacionamiento */}
                            </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ListadoColas;