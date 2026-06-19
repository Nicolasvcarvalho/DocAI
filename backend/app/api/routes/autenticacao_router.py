from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth_schema import CandidatoCreate, CandidatoCreateResponse, LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from app.schemas.base import HTTPErrorResponse

from app.services.auth_service import AuthService

router = APIRouter(prefix="/autenticacao", tags=["Autenticacao"])

@router.post(
    "/candidatos",
    response_model=CandidatoCreateResponse,
    summary="Criar conta de candidato",
    description="""
Cria uma nova conta de candidato na plataforma.

Além do cadastro do usuário, a rota realiza toda a preparação inicial
necessária para o processo documental.

---

## Objetivos da rota

A rota é responsável por:

- criar o usuário
- criar o candidato
- criar a candidatura
- calcular os documentos obrigatórios
- gerar os registros documentais iniciais

Toda a estrutura inicial é criada automaticamente pelo backend.

---

## Fluxo de criação

Fluxo executado pelo backend:

```text
Recebe dados do candidato
↓
Cria usuário
↓
Cria candidato
↓
Cria candidatura
↓
Calcula documentos obrigatórios
↓
Gera documentos pendentes
↓
Retorna dados do candidato
```

---

## Estrutura da requisição

```json
{
  "nome": "Nicolas",
  "sobrenome": "Carvalho",
  "email": "nicolas@email.com",
  "senha": "123456"
}
```

---

## Resposta de sucesso

Exemplo:

```json
{
  "id": 1,
  "nome": "Nicolas",
  "sobrenome": "Carvalho",
  "email": "nicolas@email.com",
  "tipo_usuario": "CANDIDATO",
  "mensagem": "Candidato criado com sucesso"
}
```

---

## Campos retornados

### id

Identificador do candidato criado.

---

### tipo_usuario

Perfil institucional associado à conta criada.

Atualmente sempre retorna:

```text
CANDIDATO
```

---

### mensagem

Mensagem informando que o cadastro foi concluído com sucesso.

---

## Exemplo de resposta

```json
{
  "id": 1,
  "nome": "Nicolas",
  "sobrenome": "Carvalho",
  "email": "nicolas@email.com",
  "tipo_usuario": "CANDIDATO",
  "mensagem": "Candidato criado com sucesso"
}
```
""",
    responses={

        200: {
            "model": CandidatoCreateResponse,
            "description": (
                "Candidato criado com sucesso."
            )
        },

        400: {
            "model": HTTPErrorResponse,
            "description": (
                "Erro de validação de dados."
            ),
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Email já cadastrado"
                        )
                    }
                }
            }
        }
    }
)
def salvar_candidato(dados: CandidatoCreate, db: Session = Depends(get_db)):
    
    return AuthService.criar_candidato(db, dados)

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticar usuário",
    description="""
Realiza a autenticação de um usuário na plataforma.

A autenticação é centralizada e compartilhada entre todos os perfis do sistema.

A mesma rota é utilizada por:

- candidatos
- usuários da secretaria

O backend identifica automaticamente o perfil do usuário autenticado
e retorna essa informação na resposta.

---

## Objetivos da rota

A rota é responsável por:

- validar credenciais
- autenticar o usuário
- gerar o JWT de acesso
- retornar informações básicas do usuário
- informar o perfil institucional autenticado

---

## Fluxo de autenticação

Fluxo executado pelo backend:

```text
Recebe email e senha
↓
Busca usuário pelo email
↓
Valida senha utilizando hash
↓
Gera JWT
↓
Retorna token e dados do usuário
````

---

## Estrutura da requisição

```json
{
  "email": "nicolas@email.com",
  "senha": "123456"
}
```

---

## Identificação do usuário

O sistema localiza o usuário através do email informado.

Caso o usuário exista, a senha enviada é validada contra o hash
armazenado no banco de dados.

A senha original nunca é armazenada ou retornada pelo sistema.

---

## JWT gerado

Após uma autenticação bem-sucedida, o sistema gera um JWT contendo
as informações mínimas necessárias para identificar o usuário
nas rotas protegidas.

Payload interno:

```json
{
  "sub": "1",
  "tipo_usuario": "CANDIDATO"
}
```

Onde:

* `sub` representa o identificador do usuário
* `tipo_usuario` representa o perfil institucional autenticado

Essas informações são utilizadas internamente pelo backend para:

* identificar o usuário autenticado
* aplicar regras de autorização
* controlar acesso às rotas protegidas

---

## Tipo de usuário

O campo `tipo_usuario` informa ao frontend qual perfil foi autenticado.

Exemplos:

```text
CANDIDATO

SECRETARIA
```

Essa informação pode ser utilizada pelo frontend para:

* definir redirecionamentos
* carregar áreas específicas do sistema
* renderizar menus
* exibir funcionalidades apropriadas

---

## Utilização do token

Após o login, o frontend deve armazenar o valor retornado em
`access_token`.

Todas as rotas protegidas exigem o envio desse token através do
cabeçalho Authorization.

Exemplo:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Fluxo:

```text
Login
↓
Recebe JWT
↓
Frontend armazena token
↓
Frontend envia token nas próximas requisições
↓
Backend identifica usuário autenticado
```

---

## Resposta de sucesso

Exemplo:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",

  "usuario": {
    "id": 1,
    "nome": "Nicolas",
    "sobrenome": "Carvalho",
    "tipo_usuario": "CANDIDATO"
  }
}
```

---

## Campos retornados

### access_token

JWT utilizado para autenticação das próximas requisições.

---

### token_type

Tipo do mecanismo de autenticação.

Atualmente sempre retorna:

```json
"bearer"
```

---

### usuario

Representa o usuário autenticado.

Exemplo:

```json
{
  "id": 1,
  "nome": "Nicolas",
  "sobrenome": "Carvalho",
  "tipo_usuario": "CANDIDATO"
}
```

---

## Exemplo de resposta

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",

  "usuario": {
    "id": 1,
    "nome": "Nicolas",
    "sobrenome": "Carvalho",
    "tipo_usuario": "CANDIDATO"
  }
}
```

""",
responses={

    200: {
        "model": LoginResponse,
        "description": (
            "Usuário autenticado com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Email ou senha inválidos."
        ),
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "Email ou senha inválidos"
                    )
                }
            }
        }
    }
}

)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    
    return AuthService.login(db, dados)

@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(dados: RefreshTokenRequest):

    return AuthService.refresh(dados.refresh_token)


@router.post(
    "/login_swegger",
    response_model=LoginResponse,
    include_in_schema=True,
    tags=["Auth (Swagger)"]
)
def login_swg(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    login_data = LoginRequest(
        email=dados.username,
        senha=dados.password
    )

    return AuthService.login(db, login_data)