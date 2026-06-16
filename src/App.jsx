import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login';
import Cadastro from './pages/Cadastro/Cadastro'
import DashboardCandidato from './pages/Dashboard/DashboardCandidato';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/dashboard-candidato" element={<DashboardCandidato />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;