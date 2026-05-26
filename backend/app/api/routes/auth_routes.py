from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth_schema import CandidatoCreate, CandidatoCreateResponse, LoginRequest, LoginResponse
from app.schemas.base import HTTPErrorResponse

from app.services.auth_service import AuthService

router = APIRouter()

@router.post(
    "/candidatos",
    response_model=CandidatoCreateResponse,
    status_code=200,
    summary="Criar conta de candidato",
    description="""
Cria um novo candidato no sistema.

**Fluxo de criação:**
- Cria o usuário e a entidade Candidato.
- Cria a Candidatura vinculada.
- Calcula os documentos obrigatórios com base no perfil.
- Gera os registros iniciais de documentos (status PENDENTE).
""",
    responses={
        200: {"model": CandidatoCreateResponse, "description": "Candidato criado com sucesso."},
        400: {
            "model": HTTPErrorResponse, 
            "description": "Erro de validação de dados.",
            "content": {"application/json": {"example": {"detail": "Email já cadastrado"}}}
        }
    }
)
def salvar_candidato(dados: CandidatoCreate, db: Session = Depends(get_db)):
    
    return AuthService.criar_candidato(db, dados)
    
@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login do candidato",
    description="""
Realiza a autenticação do usuário e retorna o estado atual da candidatura.

**O que o Frontend recebe:**
- **JWT (access_token):** Para ser usado no Header Authorization.
- **documentos_obrigatorios:** Uma lista completa dos documentos que o usuário deve enviar, incluindo o `id` que deve ser usado na rota de upload.
""",
    responses={
        200: {"model": LoginResponse, "description": "Login realizado com sucesso."},
        401: {
            "model": HTTPErrorResponse,
            "description": "Falha na autenticação.",
            "content": {"application/json": {"example": {"detail": "Email ou senha inválidos"}}}
        }
    }
)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    
    return AuthService.login(db, dados)


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