import { useState, useEffect, useRef } from 'react';
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
  statusBanner: {
    borderRadius: '10px',
    padding: '14px 20px',
    marginBottom: '20px',
    fontSize: '14px',
    fontWeight: '600',
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
  resumoGrid: {
    display: 'flex',
    gap: '16px',
    marginBottom: '20px',
  },
  resumoItem: {
    flex: 1,
    backgroundColor: '#252836',
    borderRadius: '8px',
    padding: '16px',
    textAlign: 'center',
  },
  resumoNumero: {
    fontSize: '28px',
    fontWeight: 'bold',
    marginBottom: '4px',
  },
  resumoLabel: {
    color: '#6b7280',
    fontSize: '12px',
  },
  progressoWrap: {
    marginTop: '8px',
  },
  progressoTopo: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '8px',
  },
  progressoTexto: {
    color: '#9ca3af',
    fontSize: '13px',
  },
  progressoPercent: {
    color: '#fff',
    fontSize: '13px',
    fontWeight: '600',
  },
  progressoBar: {
    height: '6px',
    backgroundColor: '#252836',
    borderRadius: '99px',
    overflow: 'hidden',
  },
  progressoFill: {
    height: '100%',
    backgroundColor: '#3b82f6',
    borderRadius: '99px',
    transition: 'width 0.4s ease',
  },
  docItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '14px 0',
    borderBottom: '1px solid #252836',
    gap: '12px',
  },
  docNome: {
    color: '#fff',
    fontSize: '14px',
    flex: 1,
  },
  badge: {
    padding: '4px 12px',
    borderRadius: '99px',
    fontSize: '12px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
  },
  uploadBtn: {
    backgroundColor: '#1e3a5f',
    border: '1px solid #3b82f6',
    color: '#93c5fd',
    padding: '6px 14px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '12px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
  },
  // Botão de revisar OCR — cor diferente para destacar
  ocrBtn: {
    backgroundColor: '#2d1f4e',
    border: '1px solid #a855f7',
    color: '#d8b4fe',
    padding: '6px 14px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '12px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
  },
  btnDisabled: {
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
  feedbackSucesso: {
    backgroundColor: '#0f2e1a',
    border: '1px solid #22c55e',
    color: '#86efac',
    padding: '10px 14px',
    borderRadius: '8px',
    fontSize: '13px',
    marginBottom: '16px',
  },
  feedbackErro: {
    backgroundColor: '#3b1515',
    border: '1px solid #ef4444',
    color: '#fca5a5',
    padding: '10px 14px',
    borderRadius: '8px',
    fontSize: '13px',
    marginBottom: '16px',
  },
  // Estilos do modal (compartilhado entre upload frente/verso e OCR)
  modalOverlay: {
    position: 'fixed',
    top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.7)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 999,
  },
  modalCard: {
    backgroundColor: '#1a1d27',
    borderRadius: '12px',
    padding: '32px',
    width: '100%',
    maxWidth: '480px',
    boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
    maxHeight: '90vh',
    overflowY: 'auto',
  },
  modalTitulo: {
    color: '#fff',
    fontSize: '16px',
    fontWeight: '600',
    marginBottom: '6px',
  },
  modalSubtitulo: {
    color: '#6b7280',
    fontSize: '13px',
    marginBottom: '24px',
  },
  modalBotaoUpload: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#252836',
    border: '1px dashed #374151',
    borderRadius: '8px',
    color: '#9ca3af',
    fontSize: '13px',
    cursor: 'pointer',
    marginBottom: '12px',
    textAlign: 'left',
  },
  modalBotaoUploadSelecionado: {
    border: '1px solid #22c55e',
    color: '#86efac',
    backgroundColor: '#0f2e1a',
  },
  modalBotaoEnviar: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#3b82f6',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    marginTop: '8px',
  },
  modalBotaoCancelar: {
    width: '100%',
    padding: '10px',
    backgroundColor: 'transparent',
    border: '1px solid #374151',
    color: '#9ca3af',
    borderRadius: '8px',
    fontSize: '13px',
    cursor: 'pointer',
    marginTop: '8px',
  },
  // Estilos específicos do modal OCR
  ocrLabel: {
    display: 'block',
    color: '#9ca3af',
    fontSize: '11px',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    marginBottom: '5px',
  },
  ocrInput: {
    width: '100%',
    padding: '10px 12px',
    backgroundColor: '#252836',
    border: '1px solid #374151',
    borderRadius: '8px',
    color: '#fff',
    fontSize: '14px',
    outline: 'none',
    boxSizing: 'border-box',
    marginBottom: '14px',
  },
  ocrConfirmarBtn: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#a855f7',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    marginTop: '8px',
  },
  ocrAviso: {
    backgroundColor: '#1e1040',
    border: '1px solid #a855f7',
    color: '#d8b4fe',
    padding: '10px 14px',
    borderRadius: '8px',
    fontSize: '12px',
    marginBottom: '20px',
  },
};

const statusCandidaturaConfig = {
  AGUARDANDO_DOCUMENTOS:         { cor: '#93c5fd', fundo: '#0c1f3b', texto: '📋 Aguardando documentos' },
  DOCUMENTACAO_EM_PROCESSAMENTO: { cor: '#fde68a', fundo: '#2d2006', texto: '⏳ Documentação em processamento' },
  DOCUMENTACAO_PENDENTE:         { cor: '#fde68a', fundo: '#2d2006', texto: '⚠️ Documentação pendente' },
  EM_ANALISE:                    { cor: '#c4b5fd', fundo: '#1e1040', texto: '🔍 Em análise' },
  APROVADA:                      { cor: '#86efac', fundo: '#0f2e1a', texto: '✅ Candidatura aprovada' },
  INDEFERIDA:                    { cor: '#fca5a5', fundo: '#3b1515', texto: '❌ Candidatura indeferida' },
};

const statusConfig = {
  APROVADO:               { cor: '#86efac', fundo: '#0f2e1a', texto: 'Aprovado' },
  PENDENTE_ENVIO:         { cor: '#93c5fd', fundo: '#0c1f3b', texto: 'Pendente envio' },
  ENVIADO:                { cor: '#c4b5fd', fundo: '#1e1040', texto: 'Enviado' },
  PROCESSANDO:            { cor: '#fde68a', fundo: '#2d2006', texto: 'Processando' },
  AGUARDANDO_CONFIRMACAO: { cor: '#d8b4fe', fundo: '#2d1f4e', texto: 'Revisar OCR' },
  EM_ANALISE:             { cor: '#c4b5fd', fundo: '#1e1040', texto: 'Em análise' },
  AGUARDANDO_REENVIO:     { cor: '#fca5a5', fundo: '#3b1515', texto: 'Aguard. reenvio' },
};

function DashboardCandidato() {
  const [dashboard, setDashboard] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');
  const [enviando, setEnviando] = useState(null);
  const [feedbackUpload, setFeedbackUpload] = useState({ tipo: '', mensagem: '' });
  const [docSelecionado, setDocSelecionado] = useState(null);

  const [modalFrenteVerso, setModalFrenteVerso] = useState(false);
  const [arquivoFrente, setArquivoFrente] = useState(null);
  const [arquivoVerso, setArquivoVerso] = useState(null);

  const [modalOCR, setModalOCR] = useState(false);
  const [dadosOCR, setDadosOCR] = useState(null);       
  const [dadosEditados, setDadosEditados] = useState({}); 
  const [carregandoOCR, setCarregandoOCR] = useState(false);
  const [confirmandoOCR, setConfirmandoOCR] = useState(false);

  const inputRefArquivo = useRef(null);
  const inputRefFrente = useRef(null);
  const inputRefVerso = useRef(null);

  const navigate = useNavigate();

  async function buscarDashboard() {
    try {
      const resposta = await api.get('/candidaturas/dashboard');
      setDashboard(resposta.data);
      setErro('');
    } catch (error) {
      setErro('Não foi possível carregar o dashboard.');
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    buscarDashboard();
    const intervalo = setInterval(() => buscarDashboard(), 10000);
    return () => clearInterval(intervalo);
  }, []);

  async function handleAbrirOCR(doc) {
    setDocSelecionado(doc);
    setModalOCR(true);
    setDadosOCR(null);
    setDadosEditados({});
    setCarregandoOCR(true);
    setFeedbackUpload({ tipo: '', mensagem: '' });

    try {
      const resposta = await api.get(`/ocr/documentos/${doc.id}`);
      setDadosOCR(resposta.data);

      setDadosEditados(resposta.data.dados_extraidos || {});
    } catch (error) {
      setFeedbackUpload({ tipo: 'erro', mensagem: 'Erro ao carregar dados do OCR.' });
      setModalOCR(false);
    } finally {
      setCarregandoOCR(false);
    }
  }

  async function handleConfirmarOCR() {
    setConfirmandoOCR(true);
    try {
      
      await api.post(`/ocr/documentos/${docSelecionado.id}/confirmar`, {
        dados_corrigidos: dadosEditados,
      });

      setFeedbackUpload({
        tipo: 'sucesso',
        mensagem: 'Dados confirmados! Documento enviado para análise.',
      });
      setModalOCR(false);
      buscarDashboard(); 
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao confirmar dados.';
      setFeedbackUpload({ tipo: 'erro', mensagem });
    } finally {
      setConfirmandoOCR(false);
    }
  }

  function handleClicarEnviar(doc) {
    setDocSelecionado(doc);
    setFeedbackUpload({ tipo: '', mensagem: '' });

    if (doc.aceita_frente_verso) {
      setArquivoFrente(null);
      setArquivoVerso(null);
      setModalFrenteVerso(true);
    } else {
      inputRefArquivo.current.click();
    }
  }

  function validarArquivo(arquivo) {
    const tiposPermitidos = ['image/png', 'image/jpeg'];
    if (!tiposPermitidos.includes(arquivo.type)) return 'Formato inválido. Envie PNG ou JPG.';
    const dezMB = 10 * 1024 * 1024;
    if (arquivo.size > dezMB) return 'Arquivo muito grande. Máximo 10MB.';
    return null;
  }

  async function handleArquivoUnicoSelecionado(e) {
    const arquivo = e.target.files[0];
    e.target.value = '';
    if (!arquivo || !docSelecionado) return;

    const erroValidacao = validarArquivo(arquivo);
    if (erroValidacao) { setFeedbackUpload({ tipo: 'erro', mensagem: erroValidacao }); return; }

    setEnviando(docSelecionado.id);
    try {
      const formData = new FormData();
      formData.append('tipo_documento_id', docSelecionado.tipo_documento_id);
      formData.append('arquivo', arquivo);
      await api.post('/documentos/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      setFeedbackUpload({ tipo: 'sucesso', mensagem: `"${docSelecionado.nome}" enviado! Aguardando processamento OCR.` });
      buscarDashboard();
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao enviar documento.';
      setFeedbackUpload({ tipo: 'erro', mensagem });
    } finally {
      setEnviando(null);
      setDocSelecionado(null);
    }
  }

  async function handleEnviarFrenteVerso() {
    if (!arquivoFrente || !arquivoVerso) {
      setFeedbackUpload({ tipo: 'erro', mensagem: 'Selecione a frente e o verso do documento.' });
      setModalFrenteVerso(false);
      return;
    }
    setModalFrenteVerso(false);
    setEnviando(docSelecionado.id);
    try {
      const formData = new FormData();
      formData.append('tipo_documento_id', docSelecionado.tipo_documento_id);
      formData.append('frente', arquivoFrente);
      formData.append('verso', arquivoVerso);
      await api.post('/documentos/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      setFeedbackUpload({ tipo: 'sucesso', mensagem: `"${docSelecionado.nome}" enviado! Aguardando processamento OCR.` });
      buscarDashboard();
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao enviar documento.';
      setFeedbackUpload({ tipo: 'erro', mensagem });
    } finally {
      setEnviando(null);
      setDocSelecionado(null);
      setArquivoFrente(null);
      setArquivoVerso(null);
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

      {/* Cabeçalho */}
      <div style={styles.header}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>D</div>
          <span style={styles.logoText}>DocAI</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ color: '#6b7280', fontSize: '13px' }}>Olá, {usuario.nome}</span>
          <button style={styles.sairBtn} onClick={handleSair}>Sair</button>
        </div>
      </div>

      <input ref={inputRefArquivo} type="file" accept=".png,.jpg,.jpeg" style={{ display: 'none' }} onChange={handleArquivoUnicoSelecionado} />
      <input ref={inputRefFrente} type="file" accept=".png,.jpg,.jpeg" style={{ display: 'none' }}
        onChange={(e) => {
          const arquivo = e.target.files[0]; e.target.value = '';
          if (!arquivo) return;
          const err = validarArquivo(arquivo);
          if (err) { setFeedbackUpload({ tipo: 'erro', mensagem: err }); return; }
          setArquivoFrente(arquivo);
        }}
      />
      <input ref={inputRefVerso} type="file" accept=".png,.jpg,.jpeg" style={{ display: 'none' }}
        onChange={(e) => {
          const arquivo = e.target.files[0]; e.target.value = '';
          if (!arquivo) return;
          const err = validarArquivo(arquivo);
          if (err) { setFeedbackUpload({ tipo: 'erro', mensagem: err }); return; }
          setArquivoVerso(arquivo);
        }}
      />

      {modalFrenteVerso && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalCard}>
            <p style={styles.modalTitulo}>Enviar {docSelecionado?.nome}</p>
            <p style={styles.modalSubtitulo}>Este documento exige frente e verso separados.</p>
            <button style={{ ...styles.modalBotaoUpload, ...(arquivoFrente ? styles.modalBotaoUploadSelecionado : {}) }} onClick={() => inputRefFrente.current.click()}>
              {arquivoFrente ? `✓ Frente: ${arquivoFrente.name}` : 'Selecionar frente do documento'}
            </button>
            <button style={{ ...styles.modalBotaoUpload, ...(arquivoVerso ? styles.modalBotaoUploadSelecionado : {}) }} onClick={() => inputRefVerso.current.click()}>
              {arquivoVerso ? `✓ Verso: ${arquivoVerso.name}` : 'Selecionar verso do documento'}
            </button>
            <button style={{ ...styles.modalBotaoEnviar, ...(!arquivoFrente || !arquivoVerso ? { opacity: 0.5, cursor: 'not-allowed' } : {}) }} disabled={!arquivoFrente || !arquivoVerso} onClick={handleEnviarFrenteVerso}>
              Enviar documento
            </button>
            <button style={styles.modalBotaoCancelar} onClick={() => { setModalFrenteVerso(false); setDocSelecionado(null); setArquivoFrente(null); setArquivoVerso(null); }}>
              Cancelar
            </button>
          </div>
        </div>
      )}

      {modalOCR && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalCard}>
            <p style={styles.modalTitulo}>Revisar dados do OCR</p>
            <p style={styles.modalSubtitulo}>
              {dadosOCR?.tipo_documento?.replace(/_/g, ' ')}
            </p>

            <div style={styles.ocrAviso}>
              Estes dados foram extraídos automaticamente do seu documento. Verifique se estão corretos e corrija caso necessário antes de confirmar.
            </div>

            {carregandoOCR && <p style={styles.carregandoTexto}>Carregando dados...</p>}
            {!carregandoOCR && dadosEditados && Object.keys(dadosEditados).map((campo) => (
              <div key={campo}>
                <label style={styles.ocrLabel}>{campo.replace(/_/g, ' ')}</label>
                <input
                  style={styles.ocrInput}
                  value={dadosEditados[campo] || ''}
                  onChange={(e) => setDadosEditados({ ...dadosEditados, [campo]: e.target.value })}
                />
              </div>
            ))}

            <button
              style={{
                ...styles.ocrConfirmarBtn,
                ...(confirmandoOCR ? styles.btnDisabled : {}),
              }}
              disabled={confirmandoOCR}
              onClick={handleConfirmarOCR}
            >
              {confirmandoOCR ? 'Confirmando...' : 'Confirmar dados'}
            </button>
            <button
              style={styles.modalBotaoCancelar}
              onClick={() => { setModalOCR(false); setDocSelecionado(null); }}
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      {carregando && <p style={styles.carregandoTexto}>Carregando...</p>}
      {erro && <p style={styles.erroTexto}>{erro}</p>}

      {dashboard && (
        <>
          {(() => {
            const config = statusCandidaturaConfig[dashboard.status_candidatura];
            if (!config) return null;
            return (
              <div style={{ ...styles.statusBanner, color: config.cor, backgroundColor: config.fundo }}>
                {config.texto}
              </div>
            );
          })()}

          <div style={styles.card}>
            <p style={styles.cardTitle}>Resumo documental</p>
            <div style={styles.resumoGrid}>
              <div style={styles.resumoItem}>
                <p style={{ ...styles.resumoNumero, color: '#86efac' }}>{dashboard.progresso.aprovados}</p>
                <p style={styles.resumoLabel}>Aprovados</p>
              </div>
              <div style={styles.resumoItem}>
                <p style={{ ...styles.resumoNumero, color: '#fde68a' }}>
                  {(dashboard.progresso.enviados || 0) - (dashboard.progresso.aprovados || 0) - (dashboard.progresso.aguardando_reenvio || 0)}
                </p>
                <p style={styles.resumoLabel}>Em análise</p>
              </div>
              <div style={styles.resumoItem}>
                <p style={{ ...styles.resumoNumero, color: '#fca5a5' }}>{dashboard.progresso.aguardando_reenvio || 0}</p>
                <p style={styles.resumoLabel}>Aguardando reenvio</p>
              </div>
            </div>
            <div style={styles.progressoWrap}>
              <div style={styles.progressoTopo}>
                <span style={styles.progressoTexto}>
                  {dashboard.progresso.enviados} de {dashboard.progresso.total} documentos enviados
                </span>
                <span style={styles.progressoPercent}>{dashboard.progresso.percentual}%</span>
              </div>
              <div style={styles.progressoBar}>
                <div style={{ ...styles.progressoFill, width: `${dashboard.progresso.percentual}%` }} />
              </div>
            </div>
          </div>

          <div style={styles.card}>
            <p style={styles.cardTitle}>Documentos</p>

            {feedbackUpload.mensagem && (
              <div style={feedbackUpload.tipo === 'sucesso' ? styles.feedbackSucesso : styles.feedbackErro}>
                {feedbackUpload.mensagem}
              </div>
            )}

            {dashboard.documentos.map((doc) => {
              const config = statusConfig[doc.status] || { cor: '#9ca3af', fundo: '#252836', texto: doc.status };
              const podeEnviar = doc.acoes?.pode_enviar_documento || doc.acoes?.pode_reenviar_documento;
              const podeConfirmarOCR = doc.acoes?.pode_confirmar_ocr;
              const esteEnviando = enviando === doc.id;

              return (
                <div key={doc.id} style={styles.docItem}>
                  <span style={styles.docNome}>{doc.nome}</span>

                  <span style={{ ...styles.badge, color: config.cor, backgroundColor: config.fundo }}>
                    {config.texto}
                  </span>

                  {podeConfirmarOCR && (
                    <button style={styles.ocrBtn} onClick={() => handleAbrirOCR(doc)}>
                      Revisar OCR
                    </button>
                  )}

                  {podeEnviar && !podeConfirmarOCR && (
                    <button
                      style={{ ...styles.uploadBtn, ...(esteEnviando ? styles.btnDisabled : {}) }}
                      disabled={esteEnviando}
                      onClick={() => handleClicarEnviar(doc)}
                    >
                      {esteEnviando ? 'Enviando...' : doc.acoes?.pode_reenviar_documento ? 'Reenviar' : 'Enviar'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </>
      )}

    </div>
  );
}

export default DashboardCandidato;