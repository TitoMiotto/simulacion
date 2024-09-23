import React from 'react';

const TablaListado = ({ resultados, desde, hasta, valor, ultima }) => {
    const headers = ["Visita", "Rnd_1", "Atendieron?", "Rnd_2", "Quién?", "Rnd_3", "Vendieron?", "Rnd_4", "Subscripciones", "Ganancia", "Acumulado"];

    let visita = desde;
    let acu = valor;

    // Crear tabla con encabezados
    return (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
                <tr>
                    {headers.map((header, index) => (
                        <th key={index} style={{ border: '1px solid black', padding: '8px', backgroundColor: '#917FB3', color: 'black' }}>
                            {header}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {resultados.map((resultado, index) => {
                    let [rnd_1, rnd_2, rnd_3, rnd_4, subscripciones, ganancia, flag_atend_m, flag_atend_h, flag_venta_m, flag_venta_h] = resultado;

                    let atendieron = "NO", a_quien = "", venta = "", subs = "", gana = "", acum = "";

                    if (flag_atend_m || flag_atend_h) {
                        atendieron = "SI";
                        if (flag_atend_m) {
                            a_quien = "Mujer";
                            venta = flag_venta_m ? "SI" : "NO";
                        } else if (flag_atend_h) {
                            a_quien = "Hombre";
                            venta = flag_venta_h ? "SI" : "NO";
                        }
                    }

                    rnd_2 = rnd_2 ? rnd_2.toFixed(2) : "";
                    rnd_3 = rnd_3 ? rnd_3.toFixed(2) : "";
                    rnd_4 = rnd_4 ? rnd_4.toFixed(2) : "";
                    subs = subscripciones > 0 ? subscripciones.toString() : "";
                    gana = ganancia > 0 ? ganancia.toString() : "";

                    acu += (flag_venta_m || flag_venta_h) ? 1 : 0;
                    acum = acu > 0 ? acu.toString() : "";

                    if (ultima && index === resultados.length - 1) {
                        visita = hasta;
                        acu = valor;
                    }

                    return (
                        <tr key={index}>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{visita}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{rnd_1.toFixed(2)}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{atendieron}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{rnd_2}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{a_quien}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{rnd_3}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{venta}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{rnd_4}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{subs}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{gana}</td>
                            <td style={{ border: '1px solid black', padding: '8px' }}>{acum}</td>
                        </tr>
                    );
                })}
            </tbody>
        </table>
    );
};

export default TablaListado;
