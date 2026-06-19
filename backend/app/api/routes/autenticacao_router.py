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

* candidatos
* usuários da secretaria

O backend identifica automaticamente o perfil do usuário autenticado e retorna essa informação na resposta.

---

## Objetivos da rota

A rota é responsável por:

* validar credenciais
* autenticar o usuário
* gerar o access token
* gerar o refresh token
* retornar informações básicas do usuário
* informar o perfil institucional autenticado

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
Gera access token
↓
Gera refresh token
↓
Retorna tokens e dados do usuário
```

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

Caso o usuário exista, a senha enviada é validada contra o hash armazenado no banco de dados.

A senha original nunca é armazenada ou retornada pelo sistema.

---

## Tokens gerados

Após uma autenticação bem-sucedida, o sistema gera dois JWTs:

### Access Token

Utilizado para autenticar requisições em rotas protegidas.

Possui curta duração e deve ser enviado no cabeçalho Authorization.

Payload:

```json
{
  "sub": "1",
  "tipo_usuario": "CANDIDATO",
  "type": "access"
}
```

---

### Refresh Token

Utilizado para renovar a sessão do usuário sem exigir novo login.

Possui duração maior que o access token.

Payload:

```json
{
  "sub": "1",
  "tipo_usuario": "CANDIDATO",
  "type": "refresh"
}
```

---

## Campos do payload

### sub

Representa o identificador do usuário autenticado.

Exemplo:

```json
"sub": "1"
```

---

### tipo_usuario

Representa o perfil institucional autenticado.

Exemplos:

```json
"CANDIDATO"
```

```json
"SECRETARIA"
```

Essa informação é utilizada internamente para:

* identificar o perfil autenticado;
* aplicar regras de autorização;
* restringir acesso às funcionalidades do sistema.

---

### type

Indica o tipo do token.

Possíveis valores:

```json
"access"
```

ou

```json
"refresh"
```

Esse campo permite que o backend diferencie tokens de acesso e tokens de renovação de sessão.

---

## Tipo de usuário

O campo `tipo_usuario` informa ao frontend qual perfil foi autenticado.

Exemplos:

```text
CANDIDATO

SECRETARIA
```

Essa informação pode ser utilizada pelo frontend para:

* definir redirecionamentos;
* carregar áreas específicas do sistema;
* renderizar menus;
* exibir funcionalidades apropriadas.

---

## Utilização dos tokens

Após o login, o frontend deve armazenar:

```text
access_token
refresh_token
```

---

### Access Token

Deve ser enviado em todas as rotas protegidas.

Exemplo:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Fluxo:

```text
Frontend envia access token
↓
Backend valida token
↓
Usuário autenticado
```

---

### Refresh Token

Deve ser utilizado exclusivamente para solicitar um novo access token.

Fluxo:

```text
Access token expirou
↓
Frontend envia refresh token
↓
Backend valida refresh token
↓
Novo access token é gerado
↓
Usuário continua utilizando o sistema
```

O refresh token não deve ser utilizado para acessar rotas protegidas.

---

## Renovação de sessão

Quando o access token expira, o usuário não precisa realizar login novamente.

O frontend pode utilizar o refresh token para solicitar um novo access token através da rota:

```http
POST /autenticacao/refresh
```

Fluxo:

```text
Login
↓
Recebe access token
Recebe refresh token
↓
Access token expira
↓
POST /autenticacao/refresh
↓
Novo access token
↓
Sessão continua ativa
```

---

## Resposta de sucesso

Exemplo:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
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

JWT utilizado para autenticação das rotas protegidas.

Possui curta duração.

---

### refresh_token

JWT utilizado para renovação de sessão.

Permite gerar novos access tokens sem exigir novo login.

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
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
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

## Fluxo Completo de Autenticação

```text
Login
↓
Recebe access token
Recebe refresh token
↓
Frontend armazena ambos
↓
Frontend utiliza access token nas rotas protegidas
↓
Access token expira
↓
Frontend envia refresh token
↓
Backend gera novo access token
↓
Sessão continua ativa
```

---

## Observação Arquitetural

O sistema utiliza uma estratégia de autenticação baseada em JWT stateless.

Os access tokens possuem curta duração para reduzir riscos de segurança.

Os refresh tokens possuem duração maior e permitem renovação de sessão sem exigir novo login.

Toda a infraestrutura criptográfica permanece centralizada no módulo de segurança da aplicação, responsável por:

* geração de hashes;
* validação de senhas;
* geração de access tokens;
* geração de refresh tokens;
* decodificação de JWTs.


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

@router.post("/refresh", 
             response_model=RefreshTokenResponse, 
             summary="Refresh token",
             description="""
Renova o access token de um usuário autenticado utilizando um refresh token válido.

A rota permite manter a sessão ativa sem exigir que o usuário realize um novo login quando o access token expirar.

O refresh token deve ter sido obtido previamente através da rota de autenticação.

---

## Objetivos da rota

A rota é responsável por:

* validar o refresh token recebido;
* verificar a integridade criptográfica do JWT;
* verificar a expiração do refresh token;
* validar o tipo do token recebido;
* gerar um novo access token;
* manter a sessão autenticada sem exigir novo login.

---

## Fluxo de renovação

Fluxo executado pelo backend:

```text
Recebe refresh token
↓
Valida assinatura do JWT
↓
Valida expiração
↓
Valida tipo do token
↓
Gera novo access token
↓
Retorna novo access token
```

---

## Quando utilizar

Esta rota deve ser utilizada quando o access token expirar.

Fluxo típico:

```text
Login
↓
Recebe access token
Recebe refresh token
↓
Frontend utiliza access token
↓
Access token expira
↓
Backend retorna 401
↓
Frontend chama /autenticacao/refresh
↓
Recebe novo access token
↓
Continua utilizando o sistema
```

---

## Estrutura da requisição

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## Validações realizadas

Antes de gerar um novo access token o sistema verifica:

### Assinatura do JWT

Garante que o token foi emitido pela aplicação.

Tokens adulterados são rejeitados.

---

### Expiração

O sistema verifica automaticamente se o refresh token ainda está dentro do prazo de validade.

Caso o token esteja expirado:

```json
{
  "detail": "Refresh token expirado"
}
```

---

### Tipo do Token

A rota aceita exclusivamente tokens do tipo:

```json
{
  "type": "refresh"
}
```

Caso um access token seja enviado:

```json
{
  "detail": "O token informado não é um refresh token"
}
```

---

## Geração do novo Access Token

Após todas as validações, o backend reutiliza os dados presentes no refresh token.

Payload utilizado:

```json
{
  "sub": "1",
  "tipo_usuario": "SECRETARIA"
}
```

Essas informações são utilizadas para gerar um novo access token.

Nenhuma consulta ao banco de dados é necessária.

---

## Resposta de sucesso

Exemplo:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Campos retornados

### access_token

Novo JWT utilizado para acessar rotas protegidas.

Substitui o access token expirado.

---

### token_type

Tipo do mecanismo de autenticação.

Atualmente sempre retorna:

```json
"bearer"
```

---

## Exemplo de resposta

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Segurança

A rota não aceita:

* refresh tokens expirados;
* refresh tokens adulterados;
* tokens inválidos;
* access tokens enviados indevidamente.

Todas essas situações resultam em:

```text
401 Unauthorized
```

---

## Arquitetura

A renovação de sessão é implementada utilizando JWT stateless.

O backend não armazena refresh tokens em banco de dados.

Toda a validação é realizada através:

* da assinatura criptográfica;
* do tempo de expiração;
* do tipo do token.

Essa abordagem reduz complexidade e é suficiente para o contexto atual do DocAI.

---

## Fluxo Completo

```text
Login
↓
Access Token
Refresh Token
↓
Frontend utiliza Access Token
↓
Access Token expira
↓
POST /autenticacao/refresh
↓
Refresh Token validado
↓
Novo Access Token
↓
Usuário continua autenticado
```

""", 
responses={

    200: {
        "model": RefreshTokenResponse,
        "description": (
            "Novo access token gerado com sucesso."
        )
    },

    401: {
        "model": HTTPErrorResponse,
        "description": (
            "Refresh token inválido ou expirado."
        ),
        "content": {
            "application/json": {
                "examples": {

                    "Refresh Token Expirado": {
                        "value": {
                            "detail": (
                                "Refresh token expirado"
                            )
                        }
                    },

                    "Refresh Token Invalido": {
                        "value": {
                            "detail": (
                                "Refresh token inválido"
                            )
                        }
                    },

                    "Token Nao E Refresh": {
                        "value": {
                            "detail": (
                                "Refresh token inválido"
                            )
                        }
                    }
                }
            }
        }
    }
})
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