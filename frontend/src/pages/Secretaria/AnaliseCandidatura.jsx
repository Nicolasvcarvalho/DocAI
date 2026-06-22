import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../services/api';

const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#0f1117',
    fontFamily: 'sans-serif',
    padding: '32px 24px',
    boxSizing: 'border-box',
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
    transition: 'all 0.2s',
  },
  layout: {
    display: 'flex',
    gap: '20px',
    alignItems: 'flex-start',
  },
  colunaEsquerda: {
    width: '320px',
    flexShrink: 0,
  },
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
    transition: 'all 0.2s',
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

  const [assumindoCandidatura, setAssumindoCandidatura] = useState(true);
  const [documentos, setDocumentos] = useState([]);
  const [carregandoDocs, setCarregandoDocs] = useState(false);
  const [docSelecionado, setDocSelecionado] = useState(null);

  const [detalheDoc, setDetalheDoc] = useState(null);
  const [carregandoDetalhe, setCarregandoDetalhe] = useState(false);

  const [executando, setExecutando] = useState(false);
  const [feedback, setFeedback] = useState({ tipo: '', mensagem: '' });

  const [modalCorreco, setModalCorrecao] = useState(false);
  const [motivoCorrecao, setMotivoCorrecao] = useState('');
  const [desistindo, setDesistindo] = useState(false);

  const buscarDocumentos = useCallback(async (ignorarLoadingVisual = false) => {
    if (!ignorarLoadingVisual) setCarregandoDocs(true);
    try {
      const resposta = await api.get(`/secretaria/candidaturas/${candidaturaId}/documentos`);
      setDocumentos(resposta.data.documentos || []);
    } catch (error) {
      setFeedback({ tipo: 'erro', mensagem: 'Erro ao carregar lista de documentos.' });
    } finally {
      if (!ignorarLoadingVisual) setCarregandoDocs(false);
    }
  }, [candidaturaId]);

  // Função que baixa o arquivo com autenticação e abre em nova aba
  async function handleVisualizarArquivo(arquivoId) {
    try {
      setExecutando(true);
      
      // Faz a requisição forçando o retorno em formato Blob (binário)
      const resposta = await api.get(`/secretaria/arquivos/${arquivoId}`, {
        responseType: 'blob'
      });

      // Cria uma URL temporária na memória do navegador contendo o arquivo (MIME-Type automático)
      const urlBlob = window.URL.createObjectURL(new Blob([resposta.data], { type: resposta.headers['content-type'] }));
      
      // Abre o arquivo (Imagem ou PDF) de forma nativa em uma nova aba
      window.open(urlBlob, '_blank');
      
      // Limpa a memória após um pequeno intervalo
      setTimeout(() => window.URL.revokeObjectURL(urlBlob), 100);
    } catch (error) {
      console.error("Erro ao abrir arquivo:", error);
      setFeedback({ tipo: 'erro', mensagem: 'Não foi possível carregar o arquivo original.' });
    } finally {
      setExecutando(false);
    }
  }

  useEffect(() => {
    async function inicializarAnalise() {
      try {
        setAssumindoCandidatura(true);
        setFeedback({ tipo: '', mensagem: '' });
        
        await buscarDocumentos(true);
        
      } catch (error) {
        const statusErro = error.response?.status;

        if (statusErro === 403) {
          try {
            await api.post(`/secretaria/candidaturas/${candidaturaId}/assumir`);
            await buscarDocumentos(true);
          } catch (erroAssumir) {
            const detalhe = erroAssumir.response?.data?.detail || 'Esta candidatura já está sob responsabilidade de outro analista.';
            setFeedback({ tipo: 'erro', mensagem: detalhe });
          }
        } else {
          const detalheGeral = error.response?.data?.detail || 'Erro ao carregar os dados da candidatura.';
          setFeedback({ tipo: 'erro', mensagem: detalheGeral });
        }
      } finally {
        setAssumindoCandidatura(false);
      }
    }

    if (candidaturaId) {
      inicializarAnalise();
    }
  }, [candidaturaId, buscarDocumentos]);

  async function handleSelecionarDoc(doc) {
    setDocSelecionado(doc);
    setDetalheDoc(null);
    setFeedback({ tipo: '', mensagem: '' });
    setCarregandoDetalhe(true);

    try {
      const resposta = await api.get(`/secretaria/documentos/${doc.id}`);
      let dadosSuporte = resposta.data;

      // Tratamento crucial: Se o backend devolver o OCR como string de texto, faz o parse para objeto
      if (dadosSuporte && typeof dadosSuporte.ocr === 'string') {
        try {
          dadosSuporte.ocr = JSON.parse(dadosSuporte.ocr);
        } catch (e) {
          console.error("Erro ao converter string OCR para objeto:", e);
        }
      }

      setDetalheDoc(dadosSuporte);
    } catch (error) {
      console.error("Erro ao buscar detalhe do documento:", error);
      const mensagem = error.response?.data?.detail || 'Erro ao carregar dados do documento.';
      setFeedback({ tipo: 'erro', mensagem });
    } finally {
      setCarregandoDetalhe(false);
    }
  }

async function handleAprovar() {
    // 1. Bloqueia cliques duplos imediatamente
    if (executando) return;
    
    setExecutando(true);
    setFeedback({ tipo: '', mensagem: '' });
    
    try {
      const idAnalizado = docSelecionado?.id;
      if (!idAnalizado) return;

      // Executa o POST usando uma constante local isolada do estado
      const resposta = await api.post(`/secretaria/documentos/${idAnalizado}/aprovar`);
      
      // 2. LIMPEZA ATÔMICA: Reseta as referências de memória na hora
      setDetalheDoc(null);
      setDocSelecionado(null);
      setMotivoCorrecao('');
      
      setFeedback({ tipo: 'sucesso', mensagem: resposta.data.mensagem || 'Documento aprovado!' });
      
      // 3. Redireciona para o dashboard limpo
      navigate('/dashboard-secretaria'); 
    } catch (error) {
      const mensagem = error.response?.data?.detail || 'Erro ao aprovar documento.';
      setFeedback({ tipo: 'erro', mensagem });
    } finally {
      setExecutando(false);
    }
  }

  async function handleSolicitarCorrecao() {
    if (!motivoCorrecao.trim() || executando) return;

    setExecutando(true);
    setModalCorrecao(false);
    setFeedback({ tipo: '', mensagem: '' });

    try {
      const idAnalizado = docSelecionado?.id;
      if (!idAnalizado) return;

      const resposta = await api.post(
        `/secretaria/documentos/${idAnalizado}/solicitar-correcao`,
        { motivo: motivoCorrecao }
      );
      
      // 2. LIMPEZA ATÔMICA: Reseta as referências de memória na hora
      setDetalheDoc(null);
      setDocSelecionado(null);
      setMotivoCorrecao('');
      
      setFeedback({ tipo: 'sucesso', mensagem: resposta.data.mensagem || 'Correção solicitada!' });
      
      navigate('/dashboard-secretaria');
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

  if (assumindoCandidatura) {
    return (
      <div style={styles.page}>
        <p style={styles.carregandoTexto}>Vinculando candidatura ao seu perfil de análise...</p>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>D</div>
          <span style={styles.logoText}>DocAI</span>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            style={{
              ...styles.voltarBtn,
              color: '#fca5a5',
              border: '1px solid #ef4444',
              ...(desistindo ? styles.btnDisabled : {}),
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

            {!carregandoDocs && documentos.map((doc) => {
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
          {/* Caso 1: Nenhum documento selecionado e não está carregando */}
          {!docSelecionado && !carregandoDetalhe && (
            <div style={{ ...styles.card, textAlign: 'center', padding: '60px' }}>
              <p style={{ color: '#6b7280', fontSize: '14px' }}>
                Selecione um documento na lista ao lado para analisar os dados.
              </p>
            </div>
          )}

          {/* Caso 2: Buscando dados no backend */}
          {carregandoDetalhe && (
            <p style={styles.carregandoTexto}>Carregando dados estruturados...</p>
          )}

          {/* Caso 3: Dados carregados com sucesso */}
          {detalheDoc && !carregandoDetalhe && (
            <>
              {detalheDoc?.ocr?.dados_json && Object.keys(detalheDoc.ocr.dados_json).length > 0 ? (
                <div style={styles.card}>
                  <p style={styles.cardTitle}>Dados do Candidato (Confirmados via OCR)</p>
                  
                
                  {detalheDoc?.arquivos && detalheDoc.arquivos.length > 0 && (
                    <div style={{ display: 'flex', gap: '10px', marginBottom: '16px', flexWrap: 'wrap' }}>
                      {detalheDoc.arquivos.map((arquivo) => (
                        <button
                          key={arquivo.id}
                          type="button"
                          disabled={executando}
                          onClick={() => handleVisualizarArquivo(arquivo.id)}
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '6px',
                            backgroundColor: '#1e293b',
                            border: '1px solid #475569',
                            color: '#e2e8f0',
                            padding: '10px 16px',
                            borderRadius: '8px',
                            cursor: executando ? 'not-allowed' : 'pointer',
                            fontSize: '13px',
                            fontWeight: '600',
                            opacity: executando ? 0.6 : 1
                          }}
                        >
                          Documento Original {arquivo.lado ? `(${arquivo.lado})` : ''}
                        </button>
                      ))}
                    </div>
                  )}

                  <div style={styles.ocrGrid}>
                    {Object.entries(detalheDoc.ocr.dados_json).map(([chave, valor]) => {
                      let valorTexto = '—';
                      if (valor !== null && valor !== undefined) {
                        if (typeof valor === 'object') {
                          valorTexto = JSON.stringify(valor);
                        } else {
                          valorTexto = String(valor);
                        }
                      }

                      return (
                        <div key={chave} style={styles.ocrItem}>
                          <p style={styles.ocrChave}>{String(chave).replace(/_/g, ' ')}</p>
                          <p style={styles.ocrValor}>{valorTexto}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <div style={styles.card}>
                  <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'center' }}>
                    Nenhum dado cadastral extraído para este documento.
                  </p>
                </div>
              )}

              {/* Botões de Ação baseados no status da API */}
              {(detalheDoc?.status === 'EM_ANALISE' || docSelecionado?.status === 'EM_ANALISE') && (
                <div style={styles.acoesRow}>
                  <button
                    style={{ ...styles.aprovarBtn, ...(executando ? styles.btnDisabled : {}) }}
                    disabled={executando}
                    onClick={handleAprovar}
                  >
                    {executando ? 'Processando...' : '✓ Aprovar dados'}
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