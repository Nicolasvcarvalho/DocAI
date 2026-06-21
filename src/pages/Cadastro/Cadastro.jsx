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
  row: {
    display: 'flex',
    gap: '12px',
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
  successBox: {
    backgroundColor: '#0f2e1a',
    border: '1px solid #22c55e',
    color: '#86efac',
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

function Cadastro() {
  const [nome, setNome] = useState('');
  const [sobrenome, setSobrenome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [sexo, setSexo] = useState('');
  const [dataNascimento, setDataNascimento] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');

  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');
  const [sucesso, setSucesso] = useState(false);

  const navigate = useNavigate();

  async function handleCadastro(e) {
    e.preventDefault();
    setErro('');

    if (senha !== confirmarSenha) {
      setErro('As senhas não coincidem.');
      return;
    }

    setCarregando(true);

    try {
      await api.post('/autenticacao/candidatos', { nome, sobrenome, email, senha, sexo, data_nascimento: dataNascimento });

      setSucesso(true);

      setTimeout(() => navigate('/'), 2000);

    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao criar conta. Tente novamente.';
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

        <h1 style={styles.title}>Criar conta</h1>

        {erro && <div style={styles.errorBox}>{erro}</div>}

        {sucesso && (
          <div style={styles.successBox}>
            Conta criada com sucesso! Redirecionando...
          </div>
        )}

        <form onSubmit={handleCadastro}>

          <div style={styles.row}>
            <div style={{ flex: 1 }}>
              <label style={styles.label} htmlFor="nome">Nome</label>
              <input
                id="nome"
                style={styles.input}
                type="text"
                placeholder="Maria"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                required
              />
            </div>
            <div style={{ flex: 1 }}>
              <label style={styles.label} htmlFor="sobrenome">Sobrenome</label>
              <input
                id="sobrenome"
                style={styles.input}
                type="text"
                placeholder="Silva"
                value={sobrenome}
                onChange={(e) => setSobrenome(e.target.value)}
                required
              />
            </div>
          </div>
          <label style={styles.label} htmlFor="dataNascimento">Data de nascimento</label>
          <input
            id="dataNascimento"
            style={styles.input}
            type="date"
            value={dataNascimento}
            onChange={(e) => setDataNascimento(e.target.value)}
            required
          />

          <label style={styles.label} htmlFor="sexo">Sexo</label>
          <select
            id="sexo"
            style={{ ...styles.input, cursor: 'pointer' }}
            value={sexo}
            onChange={(e) => setSexo(e.target.value)}
            required
          >
            <option value="">Selecione...</option>
            <option value="MASCULINO">Masculino</option>
            <option value="FEMININO">Feminino</option>
          </select>

          <label style={styles.label} htmlFor="email">Email</label>
          <input
            id="email"
            style={styles.input}
            type="email"
            placeholder="seu@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label style={styles.label} htmlFor="senha">Senha</label>
          <input
            id="senha"
            style={styles.input}
            type="password"
            placeholder="••••••••"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />

          <label style={styles.label} htmlFor="confirmarSenha">Confirmar senha</label>
          <input
            id="confirmarSenha"
            style={styles.input}
            type="password"
            placeholder="••••••••"
            value={confirmarSenha}
            onChange={(e) => setConfirmarSenha(e.target.value)}
            required
          />

          <Button texto="Criar conta" carregando={carregando} textoCarregando="Criando conta..." />

        </form>

        <p style={styles.footer}>
          Já possui conta?{' '}
          <a href="/" style={styles.link}>Entrar</a>
        </p>

      </div>
    </div>
  );
}

export default Cadastro;