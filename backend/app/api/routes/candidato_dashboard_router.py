from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_candidato_logado

from app.repositories.candidatura_repository import CandidaturaRepository

from app.schemas.base import HTTPErrorResponse
from app.schemas.candidatura_dashboard_schema import CandidaturaDashboardResponse

from app.services.documento.presenters.candidatura_dashboard_presenter import CandidaturaDashboardPresenter

from app.models.usuario import Usuario

router = APIRouter(prefix="/candidaturas", tags=["Dashboard Candidato"])

@router.get(
    "/dashboard",
    response_model=CandidaturaDashboardResponse,
    summary="Obter dashboard documental da candidatura",
    description="""
    Retorna o contexto documental completo da candidatura do usuário autenticado.

    A rota consolida informações operacionais e institucionais da candidatura,
    permitindo que o frontend renderize o estado atual do processo documental
    sem precisar implementar regras de negócio localmente.

    O dashboard inclui:

    * status global da candidatura
    * progresso documental
    * documentos da candidatura
    * permissões e ações disponíveis por documento

    ---

    ## Workflow da candidatura

    Fluxo principal:

    ```text
    AGUARDANDO_DOCUMENTOS
    ↓
    DOCUMENTACAO_EM_PROCESSAMENTO
    ↓
    DOCUMENTACAO_PENDENTE
    ↓
    EM_ANALISE
    ↓
    APROVADA
    ```

    Fluxo de correção documental:

    ```text
    EM_ANALISE
    ↓
    DOCUMENTACAO_PENDENTE
    ↓
    AGUARDANDO_DOCUMENTOS
    ↓
    DOCUMENTACAO_EM_PROCESSAMENTO
    ↓
    DOCUMENTACAO_PENDENTE
    ```

    Fluxo final irreversível:

    ```text
    EM_ANALISE
    ↓
    INDEFERIDA
    ```

    ---

    ## Como o status da candidatura é calculado

    O status da candidatura é derivado automaticamente a partir dos documentos obrigatórios.

    O backend recalcula esse status sempre que ocorre uma transição documental.

    Exemplos:

    ### AGUARDANDO_DOCUMENTOS

    Existe pelo menos um documento obrigatório em:

    ```text
    PENDENTE_ENVIO
    ```

    ou

    ```text
    AGUARDANDO_REENVIO
    ```

    O candidato ainda precisa realizar alguma ação.

    ---

    ### DOCUMENTACAO_EM_PROCESSAMENTO

    Todos os documentos foram enviados, porém existe pelo menos um documento em:

    ```text
    ENVIADO
    ```

    ou

    ```text
    PROCESSANDO
    ```

    ou

    ```text
    AGUARDANDO_CONFIRMACAO
    ```

    O sistema ainda está processando a documentação.

    ---

    ### DOCUMENTACAO_PENDENTE

    Existe pelo menos um documento em:

    ```text
    EM_ANALISE
    ```

    mas a candidatura ainda não foi assumida por uma secretaria.

    Nesse estado a candidatura está disponível para análise institucional.

    ---

    ### EM_ANALISE

    Existe pelo menos um documento em:

    ```text
    EM_ANALISE
    ```

    e a candidatura já foi assumida por uma secretaria através do mecanismo de lock.

    ---

    ### APROVADA

    Todos os documentos obrigatórios encontram-se em:

    ```text
    APROVADO
    ```

    ---

    ### INDEFERIDA

    A candidatura foi encerrada institucionalmente e não poderá prosseguir no fluxo.

    ---

    ## Workflow documental

    Cada documento possui um workflow próprio.

    Fluxo principal:

    ```text
    PENDENTE_ENVIO
    ↓
    ENVIADO
    ↓
    PROCESSANDO
    ↓
    AGUARDANDO_CONFIRMACAO
    ↓
    EM_ANALISE
    ↓
    APROVADO
    ```

    Fluxo de correção:

    ```text
    EM_ANALISE
    ↓
    AGUARDANDO_REENVIO
    ↓
    ENVIADO
    ↓
    PROCESSANDO
    ↓
    AGUARDANDO_CONFIRMACAO
    ↓
    EM_ANALISE
    ```

    ---

    ## Status dos documentos

    ### PENDENTE_ENVIO

    O documento ainda não foi enviado pelo candidato.

    ---

    ### ENVIADO

    O upload foi concluído com sucesso.

    ---

    ### PROCESSANDO

    O documento está sendo processado internamente.

    Exemplos:

    * OCR
    * validações técnicas
    * extração de dados

    ---

    ### AGUARDANDO_CONFIRMACAO

    O OCR foi concluído e o sistema aguarda confirmação ou correção dos dados extraídos.

    ---

    ### EM_ANALISE

    O documento está disponível para análise da secretaria.

    ---

    ### APROVADO

    O documento foi validado institucionalmente.

    ---

    ### AGUARDANDO_REENVIO

    O documento apresentou inconsistências e o candidato precisa enviar uma nova versão.

    O histórico anterior permanece preservado através do sistema de versionamento documental.

    ---

    ## Progresso documental

    O objeto `progresso` fornece métricas utilizadas pelo frontend para:

    * barras de progresso
    * indicadores percentuais
    * acompanhamento do processo
    * exibição de pendências documentais

    Exemplo:

    ```json
    {
    "total": 5,
    "enviados": 5,
    "aprovados": 3,
    "aguardando_reenvio": 1,
    "reenviados": 1,
    "percentual": 60
    }
    ```

    Onde:

    ### total

    Quantidade total de documentos da candidatura.

    ### enviados

    Quantidade de documentos que já saíram do estado `PENDENTE_ENVIO`.

    ### aprovados

    Quantidade de documentos aprovados institucionalmente.

    ### aguardando_reenvio

    Quantidade de documentos aguardando ação do candidato.

    ### reenviados

    Quantidade de documentos que já possuem mais de uma versão registrada.

    ### percentual

    Percentual de documentos aprovados em relação ao total.

    ---

    ## Ações permitidas

    Cada documento possui um conjunto de ações permitidas baseado em seu estado atual.

    Exemplo:

    ```json
    {
    "pode_visualizar_arquivo": true,
    "pode_enviar_documento": false,
    "pode_reenviar_documento": true,
    "pode_confirmar_ocr": false,
    "pode_editar_dados_ocr": false
    }
    ```

    Essas permissões permitem que o frontend renderize corretamente:

    * botões
    * estados visuais
    * bloqueios
    * CTAs
    * ações disponíveis

    sem precisar reproduzir regras de negócio localmente.

    ---

    ## Arquitetura

    O dashboard é construído utilizando:

    * Workflow Services
    * Calculators
    * Permission Services
    * Presenters

    Toda a lógica de workflow permanece centralizada no backend,
    mantendo o frontend desacoplado das regras institucionais.

    ---

    ## Exemplo de resposta

    ```json
    {
    "status_candidatura": "DOCUMENTACAO_PENDENTE",

    "progresso": {
        "total": 2,
        "enviados": 2,
        "aprovados": 0,
        "aguardando_reenvio": 0,
        "reenviados": 0,
        "percentual": 0
    },

    "documentos": [
        {
        "id": 5,
        "nome": "DOCUMENTO_IDENTIFICACAO",
        "tipo_documento_id": 1,
        "status": "EM_ANALISE",
        "aceita_frente_verso": true,

        "acoes": {
            "pode_visualizar_arquivo": true,
            "pode_enviar_documento": false,
            "pode_reenviar_documento": false,
            "pode_confirmar_ocr": false,
            "pode_editar_dados_ocr": false
        }
        }
    ]
    }
    ```

    """,
    responses={

    200: {
        "model": CandidaturaDashboardResponse,
        "description": (
            "Dashboard documental retornado com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Usuário não autenticado."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Not authenticated"
                    )
                }
            }
        }
    },

    404: {
        "model": HTTPErrorResponse,
        "description": (
            "Candidatura não encontrada."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Candidatura não encontrada"
                    )
                }
            }
        }
    },

    500: {
        "model": HTTPErrorResponse,
        "description": (
            "Estado documental inconsistente."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Status de documentos não mapeado"
                        )
                    }
                }
            }
        }
    }

)
def obter_dashboard_documental(candidato: Usuario = Depends(get_candidato_logado), db: Session = Depends(get_db)):
    
    candidatura = CandidaturaRepository.buscar_por_candidato(db, candidato.id)
    
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")

    return CandidaturaDashboardPresenter.montar_dashboard(candidatura)