import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Logo } from '../../components/Logo';
import { Button } from '../../components/Button';
import api from '../../services/api';

const styles = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0f1117',
    fontFamily: 'sans-serif',
  },
  card: {
    backgroundColor: '#1a1d27',
    padding: '40px',
    borderRadius: '12px',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
  },
  subtitle: {
    color: '#6b7280',
    fontSize: '13px',
    marginBottom: '28px',
  },
  title: {
    color: '#fff',
    fontSize: '22px',
    fontWeight: 'bold',
    marginBottom: '24px',
  },
  label: {
    display: 'block',
    color: '#9ca3af',
    fontSize: '12px',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    marginBottom: '6px',
  },
  input: {
    width: '100%',
    padding: '10px 14px',
    backgroundColor: '#252836',
    border: '1px solid #374151',
    borderRadius: '8px',
    color: '#fff',
    fontSize: '14px',
    outline: 'none',
    boxSizing: 'border-box',
    marginBottom: '16px',
  },
  errorBox: {
    backgroundColor: '#3b1515',
    border: '1px solid #ef4444',
    color: '#fca5a5',
    padding: '10px 14px',
    borderRadius: '8px',
    fontSize: '13px',
    marginBottom: '16px',
  },
  footer: {
    textAlign: 'center',
    marginTop: '20px',
    color: '#6b7280',
    fontSize: '13px',
  },
  link: {
    color: '#3b82f6',
    textDecoration: 'none',
    fontWeight: '600',
  },
};

function Login() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');

  const navigate = useNavigate();

  async function handleLogin(e) {
    e.preventDefault();
    setErro('');
    setCarregando(true);

    try {
      const resposta = await api.post('/autenticacao/login', { email, senha });

      const { access_token, usuario } = resposta.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      localStorage.setItem('usuario', JSON.stringify(usuario));

      if (usuario.tipo_usuario === 'CANDIDATO') {
        navigate('/dashboard-candidato');
      } else if (usuario.tipo_usuario === 'SECRETARIA') {
        navigate('/dashboard-secretaria');
      }
    } catch (error) {
      // Exibe a mensagem de erro retornada pela API
      const mensagem = error.response?.data?.detail || 'Email ou senha incorretos.';
      setErro(mensagem);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        <Logo/>

        <p style={styles.subtitle}>Portal documental institucional</p>

        <h1 style={styles.title}>Entrar</h1>

        {erro && <div style={styles.errorBox}>{erro}</div>}

        <form onSubmit={handleLogin}>
          <label style={styles.label} htmlFor="email">
            E-mail
          </label>
          <input
            id="email"
            style={styles.input}
            type="email"
            placeholder="seu@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label style={styles.label} htmlFor="senha">
            Senha
          </label>
          <input
            id="senha"
            style={styles.input}
            type="password"
            placeholder="••••••••"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />

          <Button texto="Entrar" carregando={carregando} textoCarregando="Entrando..." />
        </form>

        <p style={styles.footer}>
          Não possui conta?{' '}
          <a href="/cadastro" style={styles.link}>
            Criar conta
          </a>
        </p>
      </div>
    </div>
  );
}

export default Login;