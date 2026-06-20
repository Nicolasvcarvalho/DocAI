import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login';
import Cadastro from './pages/Cadastro/Cadastro'
import DashboardCandidato from './pages/Candidato/DashboardCandidato'
import DashboardSecretaria from './pages/Secretaria/DashboardSecretaria';
import AnaliseCandidatura from './pages/Secretaria/AnaliseCandidatura';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/dashboard-candidato" element={<DashboardCandidato />} />
        <Route path="/dashboard-secretaria" element={<DashboardSecretaria />} />
        <Route path="/secretaria/candidatura/:candidaturaId" element={<AnaliseCandidatura />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;