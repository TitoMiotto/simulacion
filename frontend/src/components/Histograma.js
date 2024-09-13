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
    zIndex: 3,
  };

  const ejeY = {
    ...ejeEstilo,
    bottom: 0,
    left: 0,
    height: '100%',
    width: '4px',
    zIndex: 2,
  };

  const etiquetaEstilo = {
    position: 'absolute',
    fontSize: '14px', // Fuente más grande
    color: 'black',
    backgroundColor: 'white',
    borderRadius: '5px', // Bordes redondeados
    padding: '2px 5px',
    zIndex: 2,
  };

  const etiquetasY = Array.from({ length: 5 }, (_, i) => mayor - (i * mayor / 4));

  return (
    <div style={{ padding: 50, position: 'relative' }}>
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
              left: -60,
              bottom: (4 - index) * (450 / 4) - 10,
              width: '50px',
              textAlign: 'right',
            }}
          >
            {valor}
          </div>
        ))}

        {/* Etiquetas y barras del eje X */}
        {histograma.map((intervalo, index) => {
          const ancho = 1500 / histograma.length;
          const altura = intervalo.cantidad * k;

          return (
            <div
              key={index}
              className="histograma-bar"
              title={`${intervalo.primerValor} - ${intervalo.ultimoValor}`} // Mostrar el rango completo al hacer hover
              style={{
                width: `${ancho}px`, // Barras juntas
                height: `${altura}px`,
                background: 'linear-gradient(180deg, #4facfe 0%, #00f2fe 100%)', // Gradiente para las barras
                border: '1px solid black', // Borde negro alrededor de las barras
                boxSizing: 'border-box', // Incluye el borde en el ancho de la barra
                display: 'inline-block',
                position: 'relative',
                zIndex: 1,
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  bottom: '-20px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  fontSize: '14px',
                  color: '#333',
                  fontWeight: 'bold', // Negrita para resaltar los intervalos
                  cursor: 'pointer', // Mostrar que es interactivo (hover)
                }}
              >
                {intervalo.primerValor.toFixed(2) + "-" + intervalo.ultimoValor.toFixed(2)} {/* Mostrar con menos decimales */}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Histograma;