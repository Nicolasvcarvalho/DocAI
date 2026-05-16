from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.auth_schema import CandidatoCreate, LoginRequest, LoginResponse

from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/candidatos")
def salvar_candidato(dados: CandidatoCreate, db: Session = Depends(get_db)):
    
    return AuthService.criar_candidato(db, dados)
    
@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    
    return AuthService.login(db, dados)