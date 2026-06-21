import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#0f1117',
    fontFamily: 'sans-serif',
    padding: '32px 24px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '32px',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  logoIcon: {
    width: '36px',
    height: '36px',
    backgroundColor: '#3b82f6',
    borderRadius: '8px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#fff',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  logoText: {
    color: '#fff',
    fontSize: '20px',
    fontWeight: 'bold',
  },
  sairBtn: {
    backgroundColor: 'transparent',
    border: '1px solid #374151',
    color: '#9ca3af',
    padding: '8px 16px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '13px',
  },
  card: {
    backgroundColor: '#1a1d27',
    borderRadius: '12px',
    padding: '24px',
    marginBottom: '20px',
  },
  cardTitle: {
    color: '#9ca3af',
    fontSize: '12px',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    marginBottom: '16px',
  },
  candidaturaItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px',
    backgroundColor: '#252836',
    borderRadius: '10px',
    marginBottom: '10px',
    gap: '12px',
  },
  candidaturaInfo: {
    flex: 1,
  },
  candidaturaName: {
    color: '#fff',
    fontSize: '15px',
    fontWeight: '600',
    marginBottom: '6px',
  },
  candidaturaStats: {
    display: 'flex',
    gap: '16px',
  },
  statTexto: {
    color: '#6b7280',
    fontSize: '12px',
  },
  badge: {
    padding: '4px 10px',
    borderRadius: '99px',
    fontSize: '11px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
  },
  assumirBtn: {
    backgroundColor: '#1e3a5f',
    border: '1px solid #3b82f6',
    color: '#93c5fd',
    padding: '8px 16px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
  },
  assumirBtnDisabled: {
    opacity: 0.4,
    cursor: 'not-allowed',
  },
  carregandoTexto: {
    color: '#6b7280',
    textAlign: 'center',
    padding: '40px',
  },
  erroTexto: {
    color: '#fca5a5',
    textAlign: 'center',
    padding: '40px',
  },
  vazioTexto: {
    color: '#6b7280',
    textAlign: 'center',
    padding: '40px',
    fontSize: '14px',
  },
};

function DashboardSecretaria() {
  const [candidaturas, setCandidaturas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  const [assumindo, setAssumindo] = useState(null);

  const navigate = useNavigate();

  async function buscarCandidaturas() {
    try {
      const resposta = await api.get('/secretaria/dashboard');
      setCandidaturas(resposta.data.candidaturas || resposta.data);
      setErro('');
    } catch (error) {
      setErro('Não foi possível carregar as candidaturas.');
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    buscarCandidaturas();
    const intervalo = setInterval(() => buscarCandidaturas(), 15000);
    return () => clearInterval(intervalo);
  }, []);

  async function handleAssumirCandidatura(candidaturaId) {
    setAssumindo(candidaturaId);
    try {
      await api.post(`/secretaria/candidaturas/${candidaturaId}/assumir`);

      navigate(`/secretaria/candidatura/${candidaturaId}`);
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao assumir candidatura.';
      setErro(mensagem);
      setAssumindo(null);
    }
  }

  function handleSair() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    navigate('/');
  }

  const usuario = JSON.parse(localStorage.getItem('usuario') || '{}');

  return (
    <div style={styles.page}>

      <div style={styles.header}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>D</div>
          <span style={styles.logoText}>DocAI</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ color: '#6b7280', fontSize: '13px' }}>Secretaria — {usuario.nome}</span>
          <button style={styles.sairBtn} onClick={handleSair}>Sair</button>
        </div>
      </div>

      {carregando && <p style={styles.carregandoTexto}>Carregando candidaturas...</p>}
      {erro && <p style={styles.erroTexto}>{erro}</p>}

      {!carregando && (
        <div style={styles.card}>
          <p style={styles.cardTitle}>Fila de candidaturas — aguardando análise</p>

          {candidaturas.length === 0 && (
            <p style={styles.vazioTexto}>Nenhuma candidatura disponível no momento.</p>
          )}

          {candidaturas.map((c) => (
            <div key={c.id} style={styles.candidaturaItem}>
              <div style={styles.candidaturaInfo}>
                <p style={styles.candidaturaName}>{c.nome_candidato}</p>
                <div style={styles.candidaturaStats}>
                  <span style={styles.statTexto}>
                    {c.documentos_aprovados}/{c.total_documentos} aprovados
                  </span>

                  {c.possui_reenvio && (
                    <span style={{ ...styles.badge, color: '#fde68a', backgroundColor: '#2d2006' }}>
                      Reenvio
                    </span>
                  )}
                </div>
              </div>

              <button
                style={{
                  ...styles.assumirBtn,
                  ...(assumindo === c.id ? styles.assumirBtnDisabled : {}),
                }}
                disabled={assumindo === c.id}
                onClick={() => handleAssumirCandidatura(c.id)}
              >
                {assumindo === c.id ? 'Assumindo...' : 'Analisar'}
              </button>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}

export default DashboardSecretaria;