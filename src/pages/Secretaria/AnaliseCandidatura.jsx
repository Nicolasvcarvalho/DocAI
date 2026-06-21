import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
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
  voltarBtn: {
    backgroundColor: 'transparent',
    border: '1px solid #374151',
    color: '#9ca3af',
    padding: '8px 16px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '13px',
  },
  layout: {
    display: 'flex',
    gap: '20px',
    alignItems: 'flex-start',
  },
  // Coluna esquerda — lista de documentos
  colunaEsquerda: {
    width: '260px',
    flexShrink: 0,
  },
  // Coluna direita — detalhe do documento selecionado
  colunaDireita: {
    flex: 1,
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
  docItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px',
    borderRadius: '8px',
    cursor: 'pointer',
    marginBottom: '6px',
    border: '1px solid transparent',
  },
  docItemAtivo: {
    backgroundColor: '#1e3a5f',
    border: '1px solid #3b82f6',
  },
  docNome: {
    color: '#fff',
    fontSize: '13px',
  },
  badge: {
    padding: '3px 8px',
    borderRadius: '99px',
    fontSize: '11px',
    fontWeight: '600',
  },
  // Área de visualização do arquivo
  areaImagem: {
    backgroundColor: '#252836',
    borderRadius: '10px',
    padding: '16px',
    marginBottom: '16px',
    minHeight: '200px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  imagemDoc: {
    width: '100%',
    borderRadius: '8px',
    objectFit: 'contain',
    maxHeight: '400px',
  },
  ladoLabel: {
    color: '#6b7280',
    fontSize: '11px',
    textTransform: 'uppercase',
    marginBottom: '6px',
  },
  // Dados OCR
  ocrGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '12px',
    marginBottom: '20px',
  },
  ocrItem: {
    backgroundColor: '#252836',
    borderRadius: '8px',
    padding: '12px',
  },
  ocrChave: {
    color: '#6b7280',
    fontSize: '11px',
    textTransform: 'uppercase',
    marginBottom: '4px',
  },
  ocrValor: {
    color: '#fff',
    fontSize: '14px',
    fontWeight: '500',
  },
  // Botões de ação
  acoesRow: {
    display: 'flex',
    gap: '12px',
  },
  aprovarBtn: {
    flex: 1,
    padding: '12px',
    backgroundColor: '#0f2e1a',
    border: '1px solid #22c55e',
    color: '#86efac',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
  reprovarBtn: {
    flex: 1,
    padding: '12px',
    backgroundColor: '#3b1515',
    border: '1px solid #ef4444',
    color: '#fca5a5',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
  btnDisabled: {
    opacity: 0.4,
    cursor: 'not-allowed',
  },
  // Modal de solicitação de correção
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
    maxWidth: '420px',
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
    marginBottom: '20px',
  },
  textarea: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#252836',
    border: '1px solid #374151',
    borderRadius: '8px',
    color: '#fff',
    fontSize: '14px',
    resize: 'vertical',
    minHeight: '100px',
    boxSizing: 'border-box',
    outline: 'none',
    marginBottom: '16px',
  },
  modalEnviarBtn: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#ef4444',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    marginBottom: '8px',
  },
  modalCancelarBtn: {
    width: '100%',
    padding: '10px',
    backgroundColor: 'transparent',
    border: '1px solid #374151',
    color: '#9ca3af',
    borderRadius: '8px',
    fontSize: '13px',
    cursor: 'pointer',
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
  carregandoTexto: {
    color: '#6b7280',
    textAlign: 'center',
    padding: '40px',
  },
};

const statusConfig = {
  APROVADO:          { cor: '#86efac', fundo: '#0f2e1a', texto: 'Aprovado' },
  EM_ANALISE:        { cor: '#c4b5fd', fundo: '#1e1040', texto: 'Em análise' },
  AGUARDANDO_REENVIO:{ cor: '#fca5a5', fundo: '#3b1515', texto: 'Aguard. reenvio' },
  PENDENTE:          { cor: '#fde68a', fundo: '#2d2006', texto: 'Pendente' },
};

function AnaliseCandidatura() {

  const { candidaturaId } = useParams();
  const navigate = useNavigate();

  const [documentos, setDocumentos] = useState([]);
  const [carregandoDocs, setCarregandoDocs] = useState(true);

  const [docSelecionado, setDocSelecionado] = useState(null);


  const [detalheDoc, setDetalheDoc] = useState(null);
  const [carregandoDetalhe, setCarregandoDetalhe] = useState(false);

  const [executando, setExecutando] = useState(false);
  const [feedback, setFeedback] = useState({ tipo: '', mensagem: '' });

  const [modalCorreco, setModalCorrecao] = useState(false);
  const [motivoCorrecao, setMotivoCorrecao] = useState('');

  const [desistindo, setDesistindo] = useState(false);

  async function buscarDocumentos() {
    try {
      const resposta = await api.get(`/secretaria/candidaturas/${candidaturaId}/documentos`);
      setDocumentos(resposta.data.documentos || []);
    } catch (error) {
      setFeedback({ tipo: 'erro', mensagem: 'Erro ao carregar documentos.' });
    } finally {
      setCarregandoDocs(false);
    }
  }

  useEffect(() => {
    buscarDocumentos();
  }, [candidaturaId]);


  async function handleSelecionarDoc(doc) {
    setDocSelecionado(doc);
    setDetalheDoc(null);
    setFeedback({ tipo: '', mensagem: '' });
    setCarregandoDetalhe(true);

    try {
      const resposta = await api.get(`/secretaria/documentos/${doc.id}`);
      setDetalheDoc(resposta.data);
    } catch (error) {
      setFeedback({ tipo: 'erro', mensagem: 'Erro ao carregar documento.' });
    } finally {
      setCarregandoDetalhe(false);
    }
  }

  async function handleAprovar() {
    setExecutando(true);
    setFeedback({ tipo: '', mensagem: '' });
    try {
      const resposta = await api.post(`/secretaria/documentos/${docSelecionado.id}/aprovar`);
      setFeedback({ tipo: 'sucesso', mensagem: resposta.data.mensagem || 'Documento aprovado!' });
      buscarDocumentos(); // atualiza a lista
      setDetalheDoc(null);
      setDocSelecionado(null);
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao aprovar documento.';
      setFeedback({ tipo: 'erro', mensagem });
    } finally {
      setExecutando(false);
    }
  }


  async function handleSolicitarCorrecao() {
    if (!motivoCorrecao.trim()) return;

    setExecutando(true);
    setModalCorrecao(false);
    setFeedback({ tipo: '', mensagem: '' });

    try {
      const resposta = await api.post(
        `/secretaria/documentos/${docSelecionado.id}/solicitar-correcao`,
        { motivo: motivoCorrecao }
      );
      setFeedback({ tipo: 'sucesso', mensagem: resposta.data.mensagem || 'Correção solicitada!' });
      setMotivoCorrecao('');
      buscarDocumentos();
      setDetalheDoc(null);
      setDocSelecionado(null);
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao solicitar correção.';
      setFeedback({ tipo: 'erro', mensagem });
    } finally {
      setExecutando(false);
    }
  }

  async function handleDesistir() {
  setDesistindo(true);
  try {
    await api.post(`/secretaria/candidaturas/${candidaturaId}/desistir`);
    navigate('/dashboard-secretaria');
  } catch (error) {
    const mensagem = error.response?.data?.detail || 'Erro ao desistir da análise.';
    setFeedback({ tipo: 'erro', mensagem });
  } finally {
    setDesistindo(false);
  }
}

  function urlArquivo(arquivoId) {
    const token = localStorage.getItem('token');
    return `${import.meta.env.VITE_API_URL}/secretaria/arquivos/${arquivoId}?token=${token}`;
  }

  return (
    <div style={styles.page}>

      <div style={styles.header}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>D</div>
          <span style={styles.logoText}>DocAI</span>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button style={styles.voltarBtn} onClick={() => navigate('/dashboard-secretaria')}>
            ← Voltar à fila
          </button>
          <button
            style={{
              ...styles.voltarBtn,
              color: '#fca5a5',
              border: '1px solid #ef4444',
              ...(desistindo ? { opacity: 0.4, cursor: 'not-allowed' } : {}),
            }}
            disabled={desistindo}
            onClick={handleDesistir}
          >
            {desistindo ? 'Desistindo...' : 'Desistir da análise'}
          </button>
        </div>
      </div>

      {modalCorreco && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalCard}>
            <p style={styles.modalTitulo}>Solicitar correção</p>
            <p style={styles.modalSubtitulo}>
              Informe o motivo para que o candidato saiba o que corrigir.
            </p>
            <textarea
              style={styles.textarea}
              placeholder="Ex: Documento ilegível, imagem cortada, CPF divergente..."
              value={motivoCorrecao}
              onChange={(e) => setMotivoCorrecao(e.target.value)}
            />
            <button
              style={{
                ...styles.modalEnviarBtn,
                ...(!motivoCorrecao.trim() ? styles.btnDisabled : {}),
              }}
              disabled={!motivoCorrecao.trim()}
              onClick={handleSolicitarCorrecao}
            >
              Solicitar correção
            </button>
            <button
              style={styles.modalCancelarBtn}
              onClick={() => { setModalCorrecao(false); setMotivoCorrecao(''); }}
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      {feedback.mensagem && (
        <div style={feedback.tipo === 'sucesso' ? styles.feedbackSucesso : styles.feedbackErro}>
          {feedback.mensagem}
        </div>
      )}

      <div style={styles.layout}>

        <div style={styles.colunaEsquerda}>
          <div style={styles.card}>
            <p style={styles.cardTitle}>Documentos</p>

            {carregandoDocs && <p style={styles.carregandoTexto}>Carregando...</p>}

            {documentos.map((doc) => {
              const config = statusConfig[doc.status] || { cor: '#9ca3af', fundo: '#252836', texto: doc.status };
              const ativo = docSelecionado?.id === doc.id;

              return (
                <div
                  key={doc.id}
                  style={{
                    ...styles.docItem,
                    ...(ativo ? styles.docItemAtivo : {}),
                  }}
                  onClick={() => handleSelecionarDoc(doc)}
                >
                  <span style={styles.docNome}>{doc.tipo_documento}</span>
                  <span style={{ ...styles.badge, color: config.cor, backgroundColor: config.fundo }}>
                    {config.texto}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        <div style={styles.colunaDireita}>

          {!docSelecionado && (
            <div style={{ ...styles.card, textAlign: 'center', padding: '60px' }}>
              <p style={{ color: '#6b7280', fontSize: '14px' }}>
                Selecione um documento na lista ao lado para analisar.
              </p>
            </div>
          )}

          {carregandoDetalhe && (
            <p style={styles.carregandoTexto}>Carregando documento...</p>
          )}

          {detalheDoc && !carregandoDetalhe && (
            <>
            
              <div style={styles.card}>
                <p style={styles.cardTitle}>Arquivos enviados</p>
                <div style={styles.areaImagem}>
                  {detalheDoc.arquivos.map((arquivo) => (
                    <div key={arquivo.id}>
                      {arquivo.lado && (
                        <p style={styles.ladoLabel}>{arquivo.lado}</p>
                      )}
                      <img
                        src={urlArquivo(arquivo.id)}
                        alt={arquivo.lado || 'Documento'}
                        style={styles.imagemDoc}
                      />
                    </div>
                  ))}
                </div>
              </div>

              {detalheDoc.ocr && Object.keys(detalheDoc.ocr).length > 0 && (
                <div style={styles.card}>
                  <p style={styles.cardTitle}>Dados extraídos pelo OCR</p>
                  <div style={styles.ocrGrid}>
                    {Object.entries(detalheDoc.ocr).map(([chave, valor]) => (
                      <div key={chave} style={styles.ocrItem}>
                        <p style={styles.ocrChave}>{chave.replace(/_/g, ' ')}</p>
                        <p style={styles.ocrValor}>{valor || '—'}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {detalheDoc.status === 'EM_ANALISE' && (
                <div style={styles.acoesRow}>
                  <button
                    style={{ ...styles.aprovarBtn, ...(executando ? styles.btnDisabled : {}) }}
                    disabled={executando}
                    onClick={handleAprovar}
                  >
                    {executando ? 'Processando...' : '✓ Aprovar documento'}
                  </button>
                  <button
                    style={{ ...styles.reprovarBtn, ...(executando ? styles.btnDisabled : {}) }}
                    disabled={executando}
                    onClick={() => setModalCorrecao(true)}
                  >
                    ✕ Solicitar correção
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default AnaliseCandidatura;