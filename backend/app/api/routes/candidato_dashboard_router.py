from fastapi import APIRouter, Depends, HTTPException

from textwrap import dedent

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
    description=dedent("""
    # Dashboard da Candidatura

    Retorna o estado atual da candidatura do candidato autenticado.

    A rota fornece todas as informações necessárias para exibição do processo documental no frontend.

    ---

    ## Informações retornadas

    O dashboard contém:

    * status atual da candidatura;
    * progresso documental;
    * lista de documentos;
    * ações disponíveis para cada documento.

    ---

    ## Status da candidatura

    ### AGUARDANDO_DOCUMENTOS

    O candidato ainda precisa enviar algum documento obrigatório.

    ---

    ### DOCUMENTACAO_EM_PROCESSAMENTO

    Os documentos foram enviados e estão sendo processados pelo sistema.

    ---

    ### DOCUMENTACAO_PENDENTE

    A documentação está pronta para análise da secretaria.

    ---

    ### EM_ANALISE

    A documentação está sendo analisada pela secretaria.

    ---

    ### CORRECAO_SOLICITADA

    Um ou mais documentos precisam ser corrigidos e reenviados.

    ---

    ### APROVADA

    Todos os documentos obrigatórios foram aprovados.

    ---

    ## Status dos documentos

    ### PENDENTE_ENVIO

    Documento ainda não enviado.

    ### ENVIADO

    Upload concluído.

    ### PROCESSANDO

    Documento sendo processado.

    ### AGUARDANDO_CONFIRMACAO

    Aguardando confirmação dos dados extraídos pelo OCR.

    ### EM_ANALISE

    Documento disponível para análise da secretaria.

    ### APROVADO

    Documento aprovado.

    ### AGUARDANDO_REENVIO

    Documento rejeitado e aguardando nova versão.

    ---

    ## Progresso documental

    Exemplo:

    ```json
    {
    "total": 2,
    "enviados": 2,
    "aprovados": 1,
    "rejeitados": 1,
    "reenviados": 1,
    "percentual": 50
    }
    ```

    Campos:

    * **total** → quantidade total de documentos;
    * **enviados** → documentos já enviados;
    * **aprovados** → documentos aprovados;
    * **rejeitados** → documentos aguardando reenvio;
    * **reenviados** → documentos que possuem mais de uma versão;
    * **percentual** → percentual de aprovação.

    ---

    ## Ações do documento

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

    As ações devem ser utilizadas pelo frontend para habilitar ou ocultar funcionalidades da interface.

    ---

    ## Exemplo de resposta

    ```json
    {
    "status_candidatura": "CORRECAO_SOLICITADA",
    "progresso": {
        "total": 2,
        "enviados": 2,
        "aprovados": 1,
        "rejeitados": 1,
        "reenviados": 1,
        "percentual": 50
    },
    "documentos": [
        {
        "id": 5,
        "nome": "DOCUMENTO_IDENTIFICACAO",
        "tipo_documento_id": 1,
        "status": "AGUARDANDO_REENVIO",
        "acoes": {
            "pode_visualizar_arquivo": true,
            "pode_enviar_documento": false,
            "pode_reenviar_documento": true,
            "pode_confirmar_ocr": false,
            "pode_editar_dados_ocr": false
        }
        }
    ]
    }
    ```



    """),
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