from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, BackgroundTasks

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_candidato_logado

from app.repositories.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository

from app.schemas.upload_documento_schema import DocumentoUploadInput
from app.schemas.documento_schema import DocumentoResponse
from app.schemas.base import HTTPErrorResponse

from app.services.documento.documento_service import DocumentoService
from app.services.documento.background.ocr_tasks import OCRTasks

router = APIRouter(prefix="/documentos", tags=["Documentos"])

@router.post(
    "/upload",
    response_model=DocumentoResponse,
    summary="Upload documental",
    description="""
### Fluxo Operacional

Esta rota realiza o upload dos documentos da candidatura autenticada.

Durante o processamento são executadas validações de acesso, integridade dos arquivos, regras documentais, versionamento e atualização do workflow.

---

### Regras Documentais

#### Documentos com frente e verso

Quando o tipo documental possuir:

```text
exige_frente_verso = True
```

devem ser enviados os arquivos:

* frente
* verso

Exemplos:

* Documento de identificação 

#### Documentos de arquivo único

Quando o tipo documental possuir:

```text
exige_frente_verso = False
```

deve ser enviado apenas:

* arquivo

Exemplos:

* Comprovante de residência
---

### Versionamento

Os uploads anteriores não são substituídos.

Cada novo envio gera uma nova versão do documento, preservando o histórico para fins de rastreabilidade e auditoria.

---

### Reenvio

Em caso de rejeição, um novo upload cria uma nova versão documental.

Fluxo:

```text
REJEITADO -> novo upload -> nova versão
```

---

### Workflow

Fluxo principal do documento:

```text
PENDENTE_ENVIO -> ENVIADO -> PROCESSANDO -> AGUARDANDO_CONFIRMACAO -> EM_ANALISE -> APROVADO ou REJEITADO
```

---

### Restrições

**Extensões permitidas**

* .png
* .jpg
* .jpeg

**MIME Types permitidos**

* image/png
* image/jpeg

**Tamanho máximo**

* 10 MB

---

### Controle de acesso

Antes do upload, o sistema valida:

* se a candidatura pertence ao usuário autenticado;
* se o documento pertence à candidatura informada;
* se o usuário possui permissão para acessar o recurso.

Caso alguma validação falhe, o upload é interrompido antes do início do processamento documental.

""",
    responses={

    200: {
        "model": DocumentoResponse,
        "description": (
            "Upload processado com sucesso."
        )
    },

    400: {
        "model": HTTPErrorResponse,
        "description": (
            "Erro operacional documental."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Nenhum Arquivo": {
                        "value": {
                            "detail": (
                                "Nenhum arquivo enviado."
                            )
                        }
                    },

                    "Extensao Invalida": {
                        "value": {
                            "detail": (
                                "Extensão inválida: .exe"
                            )
                        }
                    },

                    "Tipo Arquivo Invalido": {
                        "value": {
                            "detail": (
                                "Tipo de arquivo inválido"
                            )
                        }
                    },

                    "Arquivo Vazio": {
                        "value": {
                            "detail": (
                                "Arquivo vazio"
                            )
                        }
                    },

                    "Arquivo Muito Grande": {
                        "value": {
                            "detail": (
                                "Arquivo excede o tamanho máximo."
                            )
                        }
                    },

                    "Frente Verso Obrigatorio": {
                        "value": {
                            "detail": (
                                "Documento exige frente e verso"
                            )
                        }
                    },

                    "Arquivo Unico Obrigatorio": {
                        "value": {
                            "detail": (
                                "Documento exige arquivo único"
                            )
                        }
                    },

                    "Workflow Invalido": {
                        "value": {
                            "detail": (
                                "Transição de status inválida"
                            )
                        }
                    }
                }
            }
        }
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
            "Usuário não possui acesso ao recurso."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Candidatura Sem Ownership": {
                        "summary": (
                            "Usuário tentando acessar candidatura de outro usuário"
                        ),
                        "value": {
                            "detail": (
                                "Você não possui acesso a esta candidatura"
                            )
                        }
                    },

                    "Documento Sem Ownership": {
                        "summary": (
                            "Documento não pertence à candidatura"
                        ),
                        "value": {
                            "detail": (
                                "Documento não pertence à esta candidatura"
                            )
                        }
                    }
                }
            }
        }
    },

    404: {
        "model": HTTPErrorResponse,
        "description": (
            "Recurso não encontrado."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Candidatura": {
                        "value": {
                            "detail": (
                                "Candidatura não encontrada"
                            )
                        }
                    },

                    "Tipo Documental": {
                        "value": {
                            "detail": (
                                "Tipo documental não encontrado"
                            )
                        }
                    }
                }
            }
        }
    }
}
)
async def upload_documentos(
    background_tasks: BackgroundTasks,
    tipo_documento_id: int = Form(...),
    frente: UploadFile | None = File(None),
    verso: UploadFile | None = File(None),
    arquivo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    candidato = Depends(get_candidato_logado)
):
    candidatura = CandidaturaRepository.buscar_por_candidato(db, candidato_id=candidato.id)
    
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")
    
    tipo_documento = TipoDocumentoRepository.buscar_por_id(db, tipo_documento_id)

    if not tipo_documento:
        raise HTTPException(status_code=404, detail="Tipo documental não encontrado")
    
    upload_input = DocumentoUploadInput(frente=frente, verso=verso, arquivo=arquivo)

    resultado_upload = await DocumentoService.upload_documento(
        db=db,
        candidato=candidato,
        candidatura=candidatura,
        tipo_documento=tipo_documento,
        arquivos=upload_input 
    )

    background_tasks.add_task(OCRTasks.processar_documento, resultado_upload.versao_atual_id)

    return resultado_upload