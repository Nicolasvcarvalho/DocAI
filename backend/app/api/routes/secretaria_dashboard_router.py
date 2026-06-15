from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_secretaria_logada

from app.services.secretaria_dashboard_service import SecretariaDashboardService

from app.schemas.dashboard_secretaria_schema import DashboardSecretariaOutput
from app.schemas.base import HTTPErrorResponse

from app.models.usuario import Usuario

router = APIRouter(prefix="/secretaria", tags=["Secretaria Dashboard"])

@router.get("/dashboard", 
            response_model=DashboardSecretariaOutput,
            summary="Listar candidaturas disponíveis para análise",
            description="""
            Retorna a fila de candidaturas atualmente disponíveis para análise pela secretaria.

            A rota é utilizada pelo dashboard institucional para exibir as candidaturas que já concluíram o processamento documental e aguardam um analista.

            Objetivo da rota

            A rota é responsável por:

            localizar candidaturas disponíveis para análise;
            excluir candidaturas já assumidas por outro analista;
            consolidar informações resumidas da candidatura;
            calcular indicadores documentais;
            fornecer dados para construção da fila institucional.
            O que significa uma candidatura disponível?

            Uma candidatura é considerada disponível quando:

            status = DOCUMENTACAO_PENDENTE

            e

            locked_by_id = null

            Ou seja:

            existe documentação aguardando análise;
            nenhum analista assumiu a candidatura.
            Fluxo da secretaria

            Fluxo operacional:

            Candidato envia documentos
            ↓
            Processamento OCR
            ↓
            EM_ANALISE (documentos)
            ↓
            DOCUMENTACAO_PENDENTE
            ↓
            Disponível para secretaria
            ↓
            Analista assume candidatura
            ↓
            EM_ANALISE (candidatura)

            Após a candidatura ser assumida, ela deixa de aparecer nesta listagem.

            Informações retornadas

            Para cada candidatura são retornados:

            identificador da candidatura;
            nome do candidato;
            status atual da candidatura;
            quantidade total de documentos;
            quantidade de documentos aprovados;
            quantidade de documentos reenviados;
            indicador de reenvio documental.
            Indicador de reenvio

            O campo:

            {
            "possui_reenvio": true
            }

            indica que pelo menos um documento já foi reenviado pelo candidato.

            Internamente o sistema verifica se existem documentos com mais de uma versão registrada.

            Esse indicador pode ser utilizado pelo frontend para:

            destacar candidaturas com histórico de correções;
            exibir badges visuais;
            facilitar a triagem da equipe de análise.
            Estrutura da resposta

            Exemplo:

            {
            "total_candidaturas": 2,
            "candidaturas": [
                {
                "id": 1,
                "nome_candidato": "João Silva",
                "status": "DOCUMENTACAO_PENDENTE",
                "possui_reenvio": false,
                "total_documentos": 2,
                "documentos_aprovados": 0,
                "documentos_reenviados": 0
                },
                {
                "id": 2,
                "nome_candidato": "Maria Souza",
                "status": "DOCUMENTACAO_PENDENTE",
                "possui_reenvio": true,
                "total_documentos": 2,
                "documentos_aprovados": 1,
                "documentos_reenviados": 1
                }
            ]
        }
    """,
    responses={

    200: {
        "model": DashboardSecretariaOutput,
        "description": (
            "Dashboard da secretaria retornado com sucesso."
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

    403: {
        "model": HTTPErrorResponse,
        "description": (
            "Usuário não possui permissão para acessar o dashboard da secretaria."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Acesso permitido apenas para usuários da secretaria"
                    )
                }
            }
        }
    },

    500: {
        "model": HTTPErrorResponse,
        "description": (
            "Erro interno causado por inconsistência de workflow."
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
def listar_candidaturas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_secretaria_logada)):
    
    return SecretariaDashboardService.listar_candidaturas(db)