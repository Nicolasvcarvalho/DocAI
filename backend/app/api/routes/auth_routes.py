from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth_schema import CandidatoCreate, CandidatoCreateResponse, LoginRequest, LoginResponse

from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/candidatos", response_model=CandidatoCreateResponse)
def salvar_candidato(dados: CandidatoCreate, db: Session = Depends(get_db)):
    
    return AuthService.criar_candidato(db, dados)
    
@router.post("/login", response_model=LoginResponse)
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