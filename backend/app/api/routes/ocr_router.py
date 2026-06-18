from fastapi import APIRouter, Depends

from textwrap import dedent

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_candidato_logado

from app.repositories.documento_repository import DocumentoRepository

from app.schemas.ocr_review_schema import ConfirmacaoOCRSchema
from app.schemas.base import HTTPErrorResponse

from app.services.documento.permissions.DocumentoPermission import DocumentoPermission
from app.services.documento.review.ocr_review_service import OCRReviewService
from app.services.documento.validators.ocr_validator_factory import OCRValidatorFactory
from app.services.documento.review.confirmacao_ocr_service import ConfirmacaoOCRService

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.get(
        "/documentos/{documento_id}",
        summary="Obter dados extraídos pelo OCR",
        description=dedent("""
        Retorna os dados extraídos pelo mecanismo de OCR para um documento específico.

        Esta rota é utilizada durante a etapa de revisão documental, permitindo que o frontend exiba ao usuário os dados que foram identificados automaticamente a partir da imagem enviada.

        O acesso é protegido por regras de autorização, garantindo que apenas:

        * o candidato proprietário do documento;

        possam consultar os dados extraídos.

        ---

        ## Objetivo da rota

        A rota é responsável por:

        * localizar o documento solicitado;
        * validar permissões de acesso;
        * localizar o resultado OCR associado ao documento;
        * retornar os dados extraídos para exibição ou revisão.

        ---

        ## Fluxo da operação

        Fluxo executado pelo backend:

        ```text
        Recebe documento_id
        ↓
        Busca documento
        ↓
        Valida permissões de acesso
        ↓
        Busca resultado OCR
        ↓
        Retorna dados extraídos
        ```

        ---

        ## Controle de acesso

        Antes de retornar qualquer informação, o sistema valida:

        * se o documento existe;
        * se o usuário possui acesso ao documento.

        Regras:

        ### Candidato

        O candidato somente pode visualizar documentos pertencentes à sua própria candidatura.

        Caso tente acessar um documento de outra candidatura, a requisição será bloqueada.

        ---

        ## Resultado OCR

        Os dados retornados correspondem às informações extraídas automaticamente pelo OCR durante o processamento documental.

        Dependendo do tipo documental, os campos podem variar.

        Exemplos:

        ### Documento de Identificação

        ```json
        {
        "nome": "João Silva",
        "cpf": "12345678900",
        "rg": "1234567"
        }
        ```

        ### Comprovante de Residência

        ```json
        {
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "estado": "CE",
        "cep": "60000000"
        }
        ```

        ---

        ## Estrutura da resposta

        ```json
        {
        "documento_id": 1,
        "tipo_documento": "COMPROVANTE_RESIDENCIA",

        "dados_extraidos": {
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "estado": "CE",
            "cep": "60000000"
        }
        }
        ```

        ---

        ## Campos retornados

        ### documento_id

        Identificador do documento consultado.

        ---

        ### tipo_documento

        Tipo documental associado ao OCR.

        Exemplos:

        ```text
        DOCUMENTO_IDENTIFICACAO

        COMPROVANTE_RESIDENCIA
        ```

        ---

        ### dados_extraidos

        Objeto contendo os dados identificados pelo OCR.

        A estrutura varia conforme o tipo documental processado.

        ---

        ## Casos de uso

        Esta rota normalmente é utilizada para:

        * exibição dos dados extraídos;
        * revisão OCR pelo candidato;
        * correção de dados identificados incorretamente;

        ---

        ## Exemplo de resposta

        ```json
        {
        "documento_id": 1,
        "tipo_documento": "COMPROVANTE_RESIDENCIA",

        "dados_extraidos": {
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "estado": "CE",
            "cep": "60000000"
        }
        }
        ```

        """),
        responses={

        200: {
            "description": (
                "Dados OCR retornados com sucesso."
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
                "Usuário não possui acesso ao documento."
            ),
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Acesso negado ao documento"
                        )
                    }
                }
            }
        },

        404: {
            "model": HTTPErrorResponse,
            "description": (
                "Documento ou resultado OCR não encontrado."
            ),
            "content": {
                "application/json": {
                    "examples": {

                        "Documento": {
                            "value": {
                                "detail": (
                                    "Documento não encontrado"
                                )
                            }
                        },

                        "Resultado OCR": {
                            "value": {
                                "detail": (
                                    "Resultado OCR não encontrado"
                                )
                            }
                        }
                    }
                }
            }
        }
    }
    )
def buscar_dados_ocr(documento_id: int, db: Session = Depends(get_db), usuario=Depends(get_candidato_logado)):

    documento = DocumentoRepository.buscar_por_id(db, documento_id)

    DocumentoPermission.validar_acesso(documento=documento, usuario=usuario)

    return OCRReviewService.buscar_dados_ocr(db=db, documento=documento)

@router.post(
        "/documentos/{documento_id}/confirmar",
        summary="Confirmar ou corrigir dados extraídos pelo OCR",
        description=dedent("""
Permite que o candidato revisar, corrigir e confirmar os dados extraídos automaticamente pelo OCR.

Após a confirmação, o documento é enviado para análise da secretaria e a candidatura é sincronizada automaticamente.

---

## Objetivo da rota

A rota é responsável por:

* validar acesso ao documento;
* validar os dados informados;
* atualizar o resultado OCR;
* alterar o status do documento;
* sincronizar o status da candidatura.

---

## Quando utilizar

Esta rota deve ser utilizada quando o documento estiver no status:

```text
AGUARDANDO_CONFIRMACAO
```

---

## Fluxo da operação

```text
Upload
↓
OCR
↓
AGUARDANDO_CONFIRMACAO
↓
Confirmação do candidato
↓
EM_ANALISE
```

---

## Controle de acesso

### Candidato

Pode acessar apenas documentos pertencentes à própria candidatura.

---

## Validação dos dados

Os campos obrigatórios variam conforme o tipo documental.

### Documento de Identificação

Campos obrigatórios:

* nome
* cpf
* data_nascimento
* nome_pai
* nome_mae

Exemplo:

```json
{
  "dados_corrigidos": {
    "nome": "João Silva",
    "cpf": "12345678900",
    "rg": "2345678"
    "data_nascimento": "2000-01-01",
    "nome_pai": "José Silva",
    "nome_mae": "Maria Silva"
  }
}
```

### Comprovante de Residência

Campos obrigatórios:

* logradouro
* numero
* bairro
* cidade
* estado
* cep

Exemplo:

```json
{
  "dados_corrigidos": {
    "logradouro": "Rua das Flores",
    "numero": "123",
    "bairro": "Centro",
    "cidade": "Fortaleza",
    "estado": "CE",
    "cep": "60000-000"
  }
}
```
"""),
    responses={
    200: {
        "description": (
            "Dados OCR confirmados com sucesso."
        )
    },

    400: {
        "model": HTTPErrorResponse,
        "description": (
            "Erro de validação dos dados ou workflow."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Campo Obrigatorio Ausente": {
                        "value": {
                            "detail": (
                                "Campo obrigatório ausente: logradouro"
                            )
                        }
                    },

                    "Campo Obrigatorio Vazio": {
                        "value": {
                            "detail": (
                                "Campo obrigatório vazio: logradouro"
                            )
                        }
                    },

                    "Transicao Invalida": {
                        "value": {
                            "detail": (
                                "Transição de status inválida: AGUARDANDO_CONFIRMACAO -> APROVADO"
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
            "Usuário não possui acesso ao documento."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Acesso negado ao documento"
                    )
                }
            }
        }
    },

    404: {
        "model": HTTPErrorResponse,
        "description": (
            "Documento ou resultado OCR não encontrado."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Documento": {
                        "value": {
                            "detail": (
                                "Documento não encontrado"
                            )
                        }
                    },

                    "Resultado OCR": {
                        "value": {
                            "detail": (
                                "Resultado OCR não encontrado"
                            )
                        }
                    }
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
def confirmar_ocr(documento_id: int, dados: ConfirmacaoOCRSchema, db: Session = Depends(get_db), usuario=Depends(get_candidato_logado)):

    documento = DocumentoRepository.buscar_por_id(db=db, documento_id=documento_id)

    DocumentoPermission.validar_acesso(documento=documento, usuario=usuario)

    validator = OCRValidatorFactory.obter_validator(documento.tipo_documento)

    validator.validar(dados.dados_corrigidos)

    return ConfirmacaoOCRService.confirmar_ocr(db=db, documento=documento, dados_corrigidos=dados.dados_corrigidos)