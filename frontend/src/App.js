import './App.css';
import { Menu } from './components/Menu';
import { Inicio } from './components/Inicio';
import Acciones from './components/Acciones';
import Revistas from './components/Revistas';

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
            <Route path="/revistas" element={<Revistas />} />
            <Route path="*" element={<Navigate to="/inicio" replace />} />
          </Routes>
        </div>
      </BrowserRouter>


    </div>
  );
}

export default App;
