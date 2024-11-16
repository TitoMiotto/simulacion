import React from 'react';

const ListadoTablas = ({ lista }) => {
    return (
        <div className="container mt-3">
            {lista.map((item, index) => (
                <div key={index}>
                    {/* Información general */}
                    <label className="form-label">Tabla generada en el min: {item[3]}</label>
                    <br />
                    <label className="form-label">Cantidad de Vehículos esperando: {item[2]}</label>
                    <br />
                    <label className="form-label">Tipo de vehículo: {item[0]}</label>
                    
                    {/* Tabla de datos */}
                    <table className="table table-striped mt-3">
                        <thead>
                            <tr>
                                <th>t</th>
                                <th>D</th>
                                <th>dD/dt</th>
                                <th>t+1</th>
                                <th>D de t+1</th>
                            </tr>
                        </thead>
                        <tbody>
                            {/* Iterar desde el índice 3 en adelante, ya que son sublistas */}
                            {item.slice(3).map((subitem, subindex) => (
                                <tr key={subindex}>
                                    <td>{subitem[0]}</td> {/* tiempo */}
                                    <td>{subitem[1]}</td> {/* evento */}
                                    <td>{subitem[2]}</td> {/* Proxima llegada */}
                                    <td>{subitem[3]}</td> {/* rndTipoAuto */}
                                    <td>{subitem[4]}</td> {/* Auto tipo */}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ))}
        </div>
    );
};

export default ListadoTablas;
