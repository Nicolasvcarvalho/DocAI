from fastapi import APIRouter, Depends, HTTPException

from textwrap import dedent

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_secretaria_logada

from app.services.secretaria_dashboard_service import SecretariaDashboardService

from app.schemas.dashboard_secretaria_schema import DashboardSecretariaOutput
from app.schemas.base import HTTPErrorResponse
from app.schemas.secretaria.documento_analise_response import DocumentoAnaliseResponse
from app.schemas.secretaria.assumir_candidatura_schema import AssumirCandidaturaResponse
from app.schemas.secretaria.candidatura_documentos_schema import CandidaturaDocumentosResponse
from app.schemas.secretaria.analise_documento_schema import AnaliseDocumentoResponse, SolicitarCorrecaoInput

from app.models.usuario import Usuario

from app.repositories.documento_repository import DocumentoRepository
from app.repositories.arquivo_documento_repository import ArquivoDocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository

from app.services.secretaria.documento_analise_service import DocumentoAnaliseService
from app.services.secretaria.arquivo_visualizacao_service import ArquivoVisualizacaoService
from app.services.secretaria.validators.arquivo_visualizacao_validator import ArquivoVisualizacaoValidator
from app.services.secretaria.validators.candidatura_lock_validator import CandidaturaLockValidator
from app.services.secretaria.candidatura_lock_service import CandidaturaLockService
from app.services.secretaria.presenters.assumir_candidatura_presenter import AssumirCandidaturaPresenter
from app.services.secretaria.analise_documento_service import AnaliseDocumentoService
from app.services.secretaria.lock_guard_service import LockGuardService

router = APIRouter(prefix="/secretaria", tags=["Secretaria Dashboard"])

@router.get("/dashboard", 
            response_model=DashboardSecretariaOutput,
            summary="Listar candidaturas disponíveis para análise",
            description=dedent("""
Retorna a fila de candidaturas atualmente disponíveis para análise pela secretaria.

A rota é utilizada pelo dashboard institucional para exibir as candidaturas que já concluíram o processamento documental e aguardam um analista.

---

## Objetivo da rota

A rota é responsável por:

* localizar candidaturas disponíveis para análise;
* excluir candidaturas já assumidas por outro analista;
* consolidar informações resumidas da candidatura;
* calcular indicadores documentais;
* fornecer dados para construção da fila institucional.

---

## O que significa uma candidatura disponível?

Uma candidatura é considerada disponível quando:

```text
status = DOCUMENTACAO_PENDENTE

e

locked_by_id = null
```

Ou seja:

* existe documentação aguardando análise;
* nenhum analista assumiu a candidatura.

---

## Fluxo da secretaria

Fluxo operacional:

```text
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
```

Após a candidatura ser assumida, ela deixa de aparecer nesta listagem.

---

## Informações retornadas

Para cada candidatura são retornados:

* identificador da candidatura;
* nome do candidato;
* status atual da candidatura;
* quantidade total de documentos;
* quantidade de documentos aprovados;
* quantidade de documentos reenviados;
* indicador de reenvio documental.

---

## Indicador de reenvio

O campo:

```json
{
  "possui_reenvio": true
}
```

indica que pelo menos um documento já foi reenviado pelo candidato.

Internamente o sistema verifica se existem documentos com mais de uma versão registrada.

Esse indicador pode ser utilizado pelo frontend para:

* destacar candidaturas com histórico de correções;
* exibir badges visuais;
* facilitar a triagem da equipe de análise.

"""),
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
def listar_candidaturas(db: Session = Depends(get_db), secretaria: Usuario = Depends(get_secretaria_logada)):
    
    return SecretariaDashboardService.listar_candidaturas(db)


@router.get(
    "/documentos/{documento_id}",
    response_model=DocumentoAnaliseResponse,
    summary="Visualizar documento para análise",
    description="""
Retorna todas as informações necessárias para que a secretaria realize a análise de um documento.

A rota centraliza os dados documentais da versão atualmente em análise, incluindo arquivos enviados pelo candidato e os dados estruturados extraídos pelo OCR que já foram confirmados pelo usuário.

---

## Objetivo da rota

A rota é responsável por:

* localizar o documento solicitado;
* obter a versão atual do documento;
* retornar os arquivos enviados;
* retornar os dados estruturados do OCR;
* fornecer informações necessárias para análise institucional;
* permitir que a secretaria compare o documento enviado com os dados extraídos.

---

## Fluxo da análise documental

Fluxo operacional:

```text
Candidato envia documento
↓
OCR processa documento
↓
Candidato confirma dados OCR
↓
Documento entra em EM_ANALISE
↓
Secretaria consulta documento
↓
Visualiza arquivos
↓
Compara com OCR
↓
Aprova ou solicita correção
```

---

## O que é retornado

A resposta contém informações da versão atual do documento.

Entre elas:

* identificador do documento;
* status atual;
* tipo documental;
* arquivos vinculados à versão atual;
* dados estruturados extraídos pelo OCR.

---

## Dados OCR

Os dados retornados já passaram pela etapa de confirmação do candidato.

Portanto a secretaria visualiza apenas os dados estruturados finais utilizados pelo sistema.

Exemplo:

```json
{
"nome": "JOAO DA SILVA",
"cpf": "12345678900",
"rg": "1234567"
}
```

O texto bruto extraído pelo OCR não é retornado nesta rota.


---

## Estrutura da resposta

Exemplo:

```json
{
"id": 15,
"status": "EM_ANALISE",
"tipo_documento": "DOCUMENTO_IDENTIFICACAO",

"ocr": {
    "nome": "JOAO DA SILVA",
    "cpf": "12345678900",
    "rg": "1234567"
},

"arquivos": [
    {
    "id": 10,
    "lado": "FRENTE",
    "mime_type": "image/png"
    },
    {
    "id": 11,
    "lado": "FRENTE",
    "mime_type": "image/png"
}
]
}
```

---

## Regras de acesso

Esta rota é exclusiva para usuários da secretaria.

Além disso, a candidatura associada ao documento deve estar sob responsabilidade da secretaria autenticada.

Caso a candidatura esteja atribuída a outro analista, o acesso será negado.

---

## Observações

A análise sempre ocorre sobre:

```text
documento.versao_atual_id
```

Portanto, mesmo que existam versões anteriores, somente a versão atual é retornada.

Versões antigas permanecem disponíveis apenas para auditoria e histórico.
""",
    responses={
        
        200: {
            "model": DocumentoAnaliseResponse,
            "description": (
                "Documento retornado com sucesso para análise."
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
                    "examples": {

                        "Candidatura Não Assumida": {
                            "value": {
                                "detail": (
                                    "Candidatura não foi assumida"
                                )
                            }
                        },

                        "Outra Secretaria": {
                            "value": {
                                "detail": (
                                    "Candidatura está sob responsabilidade de outra secretaria"
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
                "Documento não encontrado."
            ),
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Documento não encontrado"
                        )
                    }
                }
            }
        },

        400: {
            "model": HTTPErrorResponse,
            "description": (
                "Inconsistência documental ou de workflow."
            ),
            "content": {
                "application/json": {
                    "examples": {

                        "Documento Sem Versao Atual": {
                            "value": {
                                "detail": (
                                    "Documento sem versão atual"
                                )
                            }
                        },

                        "Resultado OCR Inexistente": {
                            "value": {
                                "detail": (
                                    "Resultado OCR não encontrado para a versão atual"
                                )
                            }
                        }
                    }
                }
            }
        }
    }
)
def visualizar_documento(documento_id: int, db: Session = Depends(get_db), secretaria=Depends(get_secretaria_logada)):

    documento = DocumentoRepository.buscar_por_id(db, documento_id)

    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    
    candidatura = documento.candidatura
    LockGuardService.validar_e_renovar(db, candidatura, secretaria)
    
    return DocumentoAnaliseService.obter_documento_para_analise(documento)


@router.get(
    "/arquivos/{arquivo_id}",
    summary="Visualizar arquivo documental",
    description=dedent("""
    Retorna o conteúdo binário de um arquivo pertencente à versão atual de um documento em análise.

    A rota é utilizada pela área da secretaria para visualizar imagens e documentos PDF diretamente na interface de análise documental.

    Diferente de uma rota de download, o objetivo principal desta operação é permitir a exibição do documento dentro da aplicação para comparação com os dados estruturados extraídos pelo OCR.

    ---

    ## Objetivo da rota

    A rota é responsável por:

    * localizar o arquivo solicitado;
    * validar a integridade documental;
    * validar o vínculo do arquivo com uma candidatura;
    * validar o acesso da secretaria à candidatura;
    * verificar a existência do arquivo físico;
    * retornar o conteúdo binário do arquivo.

    ---

    ## Fluxo de visualização

    Fluxo operacional:

    ```text
    Secretaria abre documento
    ↓
    Frontend recebe URL do arquivo
    ↓
    GET /secretaria/arquivos/{arquivo_id}
    ↓
    Backend valida acesso
    ↓
    Backend localiza arquivo físico
    ↓
    Arquivo é retornado
    ↓
    Imagem ou PDF é exibido na tela
    ```

    ---

    ## Validações realizadas

    Antes de retornar o arquivo o sistema verifica:

    ```text
    Arquivo existe
    ↓
    Arquivo possui versão documental
    ↓
    Versão possui documento
    ↓
    Documento possui candidatura
    ↓
    Candidatura está válida
    ↓
    Secretaria possui acesso à candidatura
    ↓
    Arquivo físico existe
    ↓
    Retorno do arquivo
    ```

    ---

    ## Tipos suportados

    O conteúdo é retornado utilizando o MIME Type armazenado durante o upload.

    Exemplos:

    ```text
    image/png
    image/jpeg
    application/pdf
    ```

    O navegador interpreta automaticamente o tipo do conteúdo e realiza a renderização adequada.

    ---

    ## Uso pelo frontend

    Exemplo para imagens:

    ```html
    <img src="/secretaria/arquivos/15">
    ```

    Exemplo para PDF:

    ```html
    <iframe src="/secretaria/arquivos/15"></iframe>
    ```

    ---

    ## Regras de acesso

    Esta rota é exclusiva para usuários da secretaria.

    Além disso:

    * a candidatura deve estar associada ao documento;
    * a candidatura deve estar sob responsabilidade da secretaria autenticada;
    * o acesso é bloqueado para candidaturas atribuídas a outro analista.

    ---

    ## Resposta de sucesso

    Quando a requisição é bem-sucedida o backend retorna diretamente os bytes do arquivo.

    Exemplo:

    ```http
    HTTP/1.1 200 OK

    Content-Type: image/png
    ```

    ou

    ```http
    HTTP/1.1 200 OK

    Content-Type: application/pdf
    ```

    O conteúdo da resposta será o próprio arquivo.

    ---

    ## Observações

    A rota sempre trabalha sobre os arquivos vinculados à versão atualmente analisada.

    O sistema não realiza download automático.

    O comportamento padrão é permitir a visualização inline do documento para apoiar a análise institucional.
    """),
    responses={

        200: {
            "description": (
                "Arquivo retornado com sucesso."
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
                "Usuário não possui acesso ao arquivo."
            ),
            "content": {
                "application/json": {
                    "examples": {

                        "Candidatura Nao Assumida": {
                            "value": {
                                "detail": (
                                    "Candidatura não foi assumida"
                                )
                            }
                        },

                        "Outra Secretaria": {
                            "value": {
                                "detail": (
                                    "Candidatura está sob responsabilidade de outra secretaria"
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
                "Arquivo não encontrado."
            ),
            "content": {
                "application/json": {
                    "examples": {

                        "Arquivo": {
                            "value": {
                                "detail": (
                                    "Arquivo não encontrado"
                                )
                            }
                        },

                        "Arquivo Fisico": {
                            "value": {
                                "detail": (
                                    "Arquivo físico não encontrado"
                                )
                            }
                        }
                    }
                }
            }
        },

        400: {
            "model": HTTPErrorResponse,
            "description": (
                "Inconsistência documental."
            ),
            "content": {
                "application/json": {
                    "examples": {

                        "Arquivo Sem Versao": {
                            "value": {
                                "detail": (
                                    "Arquivo sem versão documental"
                                )
                            }
                        },

                        "Versao Sem Documento": {
                            "value": {
                                "detail": (
                                    "Versão sem documento"
                                )
                            }
                        },

                        "Documento Sem Candidatura": {
                            "value": {
                                "detail": (
                                    "Documento sem candidatura"
                                )
                            }
                        }
                    }
                }
            }
        }
    }
)
def visualizar_arquivo(arquivo_id: int, db: Session = Depends(get_db), secretaria=Depends(get_secretaria_logada)):

    arquivo = ArquivoDocumentoRepository.buscar_por_id(db, arquivo_id) 
      
    if not arquivo:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    candidatura = arquivo.versao_documento.documento.candidatura
    LockGuardService.validar_e_renovar(db, candidatura, secretaria)

    ArquivoVisualizacaoValidator.validar(arquivo)

    return ArquivoVisualizacaoService.visualizar(arquivo)


@router.post(
"/candidaturas/{candidatura_id}/assumir",
response_model=AssumirCandidaturaResponse,
summary="Assumir candidatura para análise documental",
description=dedent("""
Permite que uma secretaria assuma a responsabilidade pela análise documental de uma candidatura.

A operação cria um lock institucional sobre a candidatura, impedindo que outra secretaria realize análises concorrentes sobre os mesmos documentos.

---

## Objetivo da rota

A rota é responsável por:

* localizar a candidatura;
* validar se a candidatura pode ser analisada;
* verificar se não existe outra secretaria responsável;
* criar o lock institucional;
* registrar a secretaria responsável;
* atualizar o status da candidatura;
* persistir a análise no banco de dados.

---

## Fluxo de funcionamento

```text
Secretaria seleciona candidatura
↓
POST /secretaria/candidaturas/{id}/assumir
↓
Backend valida disponibilidade
↓
Backend cria lock institucional
↓
Secretaria torna-se responsável
↓
Status atualizado para EM_ANALISE
↓
Resposta retornada
```

---

## O que é o lock institucional?

O lock é um mecanismo utilizado para impedir análise concorrente.

Exemplo:

```text
Secretaria A assume candidatura
↓
lock criado
↓
Secretaria B tenta assumir
↓
acesso negado
```

Dessa forma apenas uma secretaria pode realizar alterações documentais por vez.

---

## Regras de acesso

Esta rota é exclusiva para usuários autenticados do tipo SECRETARIA.

Além disso:

* a candidatura deve existir;
* a candidatura deve estar disponível para análise;
* a candidatura não pode estar sob responsabilidade de outra secretaria.

---

## Resposta de sucesso

Exemplo:

```json
{
  "candidatura_id": 15,
  "status": "EM_ANALISE",
  "secretaria_id": 3,
  "mensagem": "Candidatura assumida com sucesso"
}
```

---

## Persistência

Quando a operação é concluída:

```text
locked_by_id
↓
preenchido

locked_at
↓
preenchido

lock_expires_at
↓
preenchido

status candidatura
↓
EM_ANALISE
```

Todas as alterações são persistidas imediatamente no banco de dados.
"""),
responses={

    200: {
        "model": AssumirCandidaturaResponse,
        "description": (
            "Candidatura assumida com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Usuário não autenticado."
        )
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

    400: {
        "model": HTTPErrorResponse,
        "description": (
            "Candidatura indisponível para análise."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "A candidatura não está disponível para análise"
                    )
                }
            }
        }
    },

    409: {
        "model": HTTPErrorResponse,
        "description": (
            "Candidatura já assumida."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Candidatura em análise por outra secretaria"
                    )
                }
            }
        }
    }
}
)

def assumir_candidatura(
    candidatura_id: int,
    db: Session = Depends(get_db),
    secretaria=Depends(get_secretaria_logada)
):

    candidatura = CandidaturaRepository.buscar_por_id(db, candidatura_id)

    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")

    candidatura = CandidaturaLockService.assumir(db=db, candidatura=candidatura, secretaria=secretaria)

    return AssumirCandidaturaPresenter.montar(candidatura)
    
@router.get(
"/candidaturas/{candidatura_id}/documentos",
response_model=CandidaturaDocumentosResponse,
summary="Listar documentos da candidatura",
description=dedent("""
Retorna todos os documentos pertencentes a uma candidatura assumida pela secretaria autenticada.

A rota é utilizada como ponto de entrada para a análise documental, permitindo que a secretaria visualize quais documentos precisam ser avaliados.

---

## Objetivo da rota

A rota é responsável por:

* localizar a candidatura;
* validar o lock institucional;
* validar a secretaria responsável;
* listar todos os documentos da candidatura;
* retornar o status atual de cada documento.

---

## Fluxo de funcionamento

```text
Secretaria assume candidatura
↓
GET /secretaria/candidaturas/{id}/documentos
↓
Backend valida lock
↓
Backend valida secretaria responsável
↓
Documentos são carregados
↓
Lista retornada
```

---

## Informações retornadas

Para cada documento são retornados:

* identificador do documento;
* tipo documental;
* status atual do workflow.

Exemplo:

```json
{
  "candidatura_id": 15,
  "documentos": [
    {
      "id": 10,
      "tipo_documento": "DOCUMENTO_IDENTIFICACAO",
      "status": "EM_ANALISE"
    },
    {
      "id": 11,
      "tipo_documento": "COMPROVANTE_RESIDENCIA",
      "status": "APROVADO"
    }
  ]
}
```

---

## Regras de acesso

Esta rota é exclusiva para usuários da secretaria.

Além disso:

* a candidatura deve existir;
* a candidatura deve estar assumida;
* a secretaria autenticada deve ser a responsável pela candidatura.

---

## Renovação automática do lock

Sempre que a secretaria acessar informações da candidatura o lock institucional pode ser renovado.

Isso evita que a candidatura seja liberada enquanto está sendo efetivamente analisada.
"""),
responses={

    200: {
        "model": CandidaturaDocumentosResponse,
        "description": (
            "Documentos retornados com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Usuário não autenticado."
        )
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

    403: {
        "model": HTTPErrorResponse,
        "description": (
            "Acesso negado à candidatura."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Nao Assumida": {
                        "value": {
                            "detail": (
                                "Candidatura não foi assumida"
                            )
                        }
                    },

                    "Outra Secretaria": {
                        "value": {
                            "detail": (
                                "Candidatura está sob responsabilidade de outra secretaria"
                            )
                        }
                    }
                }
            }
        }
    }
}
)
def listar_documentos_candidatura(candidatura_id: int, db: Session = Depends(get_db), secretaria=Depends(get_secretaria_logada)):
    
    candidatura = CandidaturaRepository.buscar_por_id(db, candidatura_id)

    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada")

    CandidaturaLockValidator.validar(candidatura, secretaria)

    return {
        "candidatura_id": candidatura.id,
        "documentos": [
            {
                "id": documento.id,
                "tipo_documento": documento.tipo_documento.nome,
                "status": documento.status
            }
            for documento in candidatura.documentos
        ]
    }

@router.post(
"/documentos/{documento_id}/aprovar",
response_model=AnaliseDocumentoResponse,
summary="Aprovar documento",
description=dedent("""
Registra a aprovação de um documento durante a análise documental.

A operação cria um registro formal de análise, atualiza o workflow documental e recalcula automaticamente o status da candidatura.

---

## Objetivo da rota

A rota é responsável por:

* localizar o documento;
* validar o lock institucional;
* validar a secretaria responsável;
* registrar a decisão da análise;
* aprovar o documento;
* recalcular o status da candidatura;
* liberar o lock quando apropriado;
* persistir todas as alterações no banco de dados.

---

## Fluxo de aprovação

```text
Secretaria abre documento
↓
Analisa arquivo e OCR
↓
POST /secretaria/documentos/{id}/aprovar
↓
Registro AnaliseDocumento criado
↓
Documento marcado como APROVADO
↓
Status da candidatura recalculado
↓
Alterações persistidas
```

---

## Registro de auditoria

Toda aprovação gera um registro permanente:

```text
AnaliseDocumento
↓
versão analisada
↓
secretaria responsável
↓
resultado da análise
↓
data da decisão
```

Isso garante rastreabilidade institucional.

---

## Atualização automática do workflow

Após a aprovação:

```text
Documento
↓
APROVADO
```

O sistema recalcula automaticamente:

```text
Status da candidatura
```

Possíveis resultados:

```text
EM_ANALISE
```

ou

```text
APROVADA
```

dependendo dos demais documentos obrigatórios.

---

## Resposta de sucesso

Exemplo:

```json
{
  "documento_id": 10,
  "status_documento": "APROVADO",
  "status_candidatura": "EM_ANALISE",
  "mensagem": "Documento aprovado com sucesso"
}
```

---

## Regras de acesso

Esta rota é exclusiva para usuários da secretaria.

Além disso:

* o documento deve existir;
* a candidatura deve estar assumida;
* a secretaria autenticada deve ser a responsável pela candidatura;
* o lock institucional deve estar válido.

---

## Persistência

Todas as alterações realizadas pela rota são persistidas imediatamente no banco de dados.

Uma aprovação não é removida caso o lock expire posteriormente.
"""),
responses={

    200: {
        "model": AnaliseDocumentoResponse,
        "description": (
            "Documento aprovado com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Usuário não autenticado."
        )
    },

    404: {
        "model": HTTPErrorResponse,
        "description": (
            "Documento não encontrado."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Documento não encontrado"
                    )
                }
            }
        }
    },

    403: {
        "model": HTTPErrorResponse,
        "description": (
            "Acesso negado ao documento."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Nao Assumida": {
                        "value": {
                            "detail": (
                                "Candidatura não foi assumida"
                            )
                        }
                    },

                    "Outra Secretaria": {
                        "value": {
                            "detail": (
                                "Candidatura está sob responsabilidade de outra secretaria"
                            )
                        }
                    }
                }
            }
        }
    }
}
)
def aprovar_documento(documento_id: int, db: Session = Depends(get_db), secretaria=Depends(get_secretaria_logada)):

    documento = DocumentoRepository.buscar_por_id(db, documento_id)
    
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    
    candidatura = documento.candidatura
    LockGuardService.validar_e_renovar(db, candidatura, secretaria)


    return AnaliseDocumentoService.aprovar(db=db, documento=documento, secretaria=secretaria)


@router.post(
"/documentos/{documento_id}/solicitar-correcao",
response_model=AnaliseDocumentoResponse,
summary="Solicitar correção documental",
description=dedent("""
Registra uma reprovação documental e solicita o reenvio do documento pelo candidato.

A operação cria um registro formal de análise, armazena o motivo da correção, atualiza o workflow documental e recalcula automaticamente o status da candidatura.

---

## Objetivo da rota

A rota é responsável por:

* localizar o documento;
* validar o lock institucional;
* validar a secretaria responsável;
* registrar a decisão da análise;
* armazenar o motivo da correção;
* alterar o status do documento;
* recalcular o status da candidatura;
* liberar o lock quando apropriado;
* persistir todas as alterações no banco de dados.

---

## Fluxo de solicitação de correção

```text
Secretaria abre documento
↓
Analisa arquivo e OCR
↓
Identifica inconsistência
↓
POST /secretaria/documentos/{id}/solicitar-correcao
↓
Registro AnaliseDocumento criado
↓
Motivo armazenado
↓
Documento marcado como AGUARDANDO_REENVIO
↓
Status da candidatura recalculado
↓
Alterações persistidas
```

---

## Estrutura da requisição

Exemplo:

```json
{
  "motivo": "Documento ilegível"
}
```

---

## Campo motivo

O motivo é utilizado para informar ao candidato exatamente o que precisa ser corrigido.

Exemplos:

```text
Documento ilegível
```

```text
Imagem cortada
```

```text
CPF divergente dos dados cadastrados
```

```text
Verso do documento não enviado
```

Essas informações serão utilizadas pelo candidato durante o processo de reenvio documental.

---

## Registro de auditoria

Toda solicitação de correção gera um registro permanente:

```text
AnaliseDocumento
↓
versão analisada
↓
secretaria responsável
↓
resultado da análise
↓
motivo informado
↓
data da decisão
```

Isso garante rastreabilidade completa do processo documental.

---

## Atualização automática do workflow

Após a solicitação de correção:

```text
Documento
↓
AGUARDANDO_REENVIO
```

O candidato passa a visualizar:

```text
Reenviar Documento
```

em seu painel documental.

---

## Atualização da candidatura

Após a alteração do documento o sistema recalcula automaticamente o status da candidatura.

Possíveis resultados:

```text
AGUARDANDO_DOCUMENTOS
```

ou

```text
EM_ANALISE
```

dependendo do estado dos demais documentos obrigatórios.

---

## Resposta de sucesso

Exemplo:

```json
{
  "documento_id": 10,
  "status_documento": "AGUARDANDO_REENVIO",
  "status_candidatura": "AGUARDANDO_DOCUMENTOS",
  "mensagem": "Correção documental solicitada com sucesso"
}
```

---

## Regras de acesso

Esta rota é exclusiva para usuários da secretaria.

Além disso:

* o documento deve existir;
* a candidatura deve estar assumida;
* a secretaria autenticada deve ser a responsável pela candidatura;
* o lock institucional deve estar válido.

---

## Persistência

Todas as alterações realizadas pela rota são persistidas imediatamente no banco de dados.

O histórico da análise permanece armazenado mesmo após:

```text
expiração do lock
```

ou

```text
troca da secretaria responsável
```

garantindo a integridade institucional do processo.

---

## Relação com o reenvio

Após a solicitação de correção o fluxo segue:

```text
Documento aprovado?
↓ Não

AGUARDANDO_REENVIO
↓
Candidato visualiza motivo
↓
Novo upload
↓
Nova versão documental
↓
Novo OCR
↓
Nova análise da secretaria
```

O documento original não é sobrescrito.

Cada novo envio gera uma nova versão documental, preservando todo o histórico da candidatura.
"""),
responses={

    200: {
        "model": AnaliseDocumentoResponse,
        "description": (
            "Correção documental solicitada com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Usuário não autenticado."
        )
    },

    404: {
        "model": HTTPErrorResponse,
        "description": (
            "Documento não encontrado."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Documento não encontrado"
                    )
                }
            }
        }
    },

    403: {
        "model": HTTPErrorResponse,
        "description": (
            "Acesso negado ao documento."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Candidatura Nao Assumida": {
                        "value": {
                            "detail": (
                                "Candidatura não foi assumida"
                            )
                        }
                    },

                    "Outra Secretaria": {
                        "value": {
                            "detail": (
                                "Candidatura está sob responsabilidade de outra secretaria"
                            )
                        }
                    }
                }
            }
        }
    },

    400: {
        "model": HTTPErrorResponse,
        "description": (
            "Erro de validação da análise."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Motivo Obrigatorio": {
                        "value": {
                            "detail": (
                                "O motivo da correção é obrigatório"
                            )
                        }
                    }
                }
            }
        }
    }
}
)
def solicitar_correcao(
    documento_id: int,
    dados: SolicitarCorrecaoInput,
    db: Session = Depends(get_db),
    secretaria=Depends(get_secretaria_logada)
):

    documento = DocumentoRepository.buscar_por_id(db, documento_id)

    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")    
    
    candidatura = documento.candidatura
    LockGuardService.validar_e_renovar(db, candidatura, secretaria)

    return AnaliseDocumentoService.solicitar_correcao(
        db=db,
        documento=documento,
        secretaria=secretaria,
        motivo=dados.motivo
    )