import './App.css';
import { Menu } from './components/Menu';
import { Inicio } from './components/Inicio';
import Acciones from './components/Acciones';
import MonteCarlo from './components/Montecarlo';
import Colas from './components/Colas';
import Colas2 from './components/Colas2'; // Importa el nuevo componente

import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Menu />
        <div className="divBody">
          <Routes>
            <Route path="/inicio" element={<Inicio />} />
            <Route path="/acciones" element={<Acciones />} />
            <Route path="/monteCarlo" element={<MonteCarlo />} />
            <Route path="/colas" element={<Colas />} />
            <Route path="/colas2" element={<Colas2/>} />
            <Route path="*" element={<Navigate to="/inicio" replace />} />
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
