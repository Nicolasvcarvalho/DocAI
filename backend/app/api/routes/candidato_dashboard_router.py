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

- status global da candidatura
- progresso documental
- documentos da candidatura
- permissões e ações disponíveis por documento

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
DOCUMENTACAO_EM_PROCESSAMENTO
```

Fluxo final irreversível:

```text
EM_ANALISE
↓
INDEFERIDA
```

---

## Status da candidatura

### AGUARDANDO_DOCUMENTOS

A candidatura ainda não possui todos os documentos obrigatórios enviados.

---

### DOCUMENTACAO_EM_PROCESSAMENTO

Todos os documentos obrigatórios foram enviados e o sistema está executando:

- OCR
- validações
- processamento técnico
- detecção de inconsistências

---

### DOCUMENTACAO_PENDENTE

O processamento técnico foi concluído e a candidatura aguarda:

- análise institucional
- correção documental
- reenvio de documentos

---

### EM_ANALISE

A candidatura está sob análise ativa da secretaria.

---

### APROVADA

Todos os documentos foram validados e a candidatura foi aprovada institucionalmente.

---

### INDEFERIDA

A candidatura foi recusada de forma definitiva.

---

## Workflow documental

Cada documento possui um workflow próprio:

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
APROVADO | REJEITADO
```

---

## Progresso documental

O objeto `progresso` fornece métricas utilizadas pelo frontend para:

- barras de progresso
- indicadores percentuais
- pendências documentais
- acompanhamento do processo

Exemplo:

```json
{
  "total": 5,
  "enviados": 5,
  "aprovados": 3,
  "rejeitados": 1,
  "percentual": 60
}
```

---

## Ações permitidas

Cada documento possui um conjunto de ações permitidas baseado no seu estado atual.

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

- botões
- bloqueios
- CTAs
- estados visuais
- ações disponíveis

sem replicar regras de negócio localmente.

---

## Arquitetura

O dashboard é montado utilizando:

- workflow services
- calculators
- permission services
- presenters

Toda a lógica de workflow permanece centralizada no backend,
mantendo o frontend desacoplado das regras institucionais.

---

## Exemplo de resposta

```json
{
  "status_candidatura": "DOCUMENTACAO_PENDENTE",

  "progresso": {
    "total": 5,
    "enviados": 5,
    "aprovados": 3,
    "rejeitados": 1,
    "percentual": 60
  },

  "documentos": [
    {
      "id": 1,
      "nome": "DOCUMENTO_IDENTIFICACAO",
      "status": "REJEITADO",
      "aceita_frente_verso": "True"

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
        }
    }
)
def obter_dashboard_documental(candidato: Usuario = Depends(get_candidato_logado), db: Session = Depends(get_db)):
    
    candidatura = CandidaturaRepository.buscar_por_candidato(db, candidato.id)
    
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")

    return CandidaturaDashboardPresenter.montar_dashboard(candidatura)