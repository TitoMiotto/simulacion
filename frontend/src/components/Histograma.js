import React from 'react';

const Histograma = ({ histograma }) => {
  let mayor = 0;
  histograma.forEach(e => {
    if (e.cantidad > mayor) {
      mayor = e.cantidad;
    }
  });
  let k = 450 / mayor;

  // Estilos para los ejes y etiquetas
  const ejeEstilo = {
    position: 'absolute',
    backgroundColor: 'black',
  };

  const ejeX = {
    ...ejeEstilo,
    bottom: 0,
    left: 0,
    width: '100%',
    height: '4px',
    zIndex: 3, // Eje X arriba de todos
  };

  const ejeY = {
    ...ejeEstilo,
    bottom: 0,
    left: 0,
    height: '100%',
    width: '4px',
    zIndex: 2, // Eje Y debajo del eje X pero arriba del histograma
  };

  // Estilo para las etiquetas
  const etiquetaEstilo = {
    position: 'absolute',
    fontSize: '12px',
    color: 'black',
    backgroundColor: 'white',
    padding: '2px',
    zIndex: 2, // Etiquetas del eje Y arriba del histograma pero debajo del eje X
  };

  // Obtener los valores máximos del eje Y
  const etiquetasY = Array.from({ length: 5 }, (_, i) => mayor - (i * mayor / 4));

  return (
    <div style={{ padding: 150, position: 'relative' }}>
      <div className="histograma-container" style={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-end', position: 'relative' }}>
        {/* Eje X */}
        <div style={ejeX}></div>

        {/* Eje Y */}
        <div style={ejeY}></div>

        {/* Etiquetas del eje Y */}
        {etiquetasY.map((valor, index) => (
          <div
            key={`etiquetaY-${index}`}
            style={{
              ...etiquetaEstilo,
              left: -50, // Ajusta la posición horizontal de las etiquetas Y
              bottom: (4 - index) * (450 / 4) - 10, // Ajusta la posición vertical
              width: '50px',
              textAlign: 'right',
            }}
          >
            {valor}
          </div>
        ))}

        {/* Etiquetas del eje X */}
        {histograma.map((intervalo, index) => {
          const ancho = 1500 / histograma.length;
          const altura = intervalo.cantidad * k;

          return (
            <div
              key={index}
              className="histograma-bar"
              style={{
                width: `${ancho}px`,
                height: `${altura}px`,
                backgroundColor: '#8884d8',
                display: 'inline-block',
                position: 'relative',
                zIndex: 1, // Barras del histograma debajo de los ejes
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  bottom: '-20px', // Ajusta la posición vertical de las etiquetas X
                  left: '50%',
                  transform: 'translateX(-50%)',
                  fontSize: '12px',
                }}
              >
                {intervalo.primerValor + "-" + intervalo.ultimoValor} {/* Muestra el primerValor del intervalo */}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Histograma;
