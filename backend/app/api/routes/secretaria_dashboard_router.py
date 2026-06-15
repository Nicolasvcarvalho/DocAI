from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import get_secretaria_logada

from app.services.secretaria_dashboard_service import SecretariaDashboardService

from app.schemas.dashboard_secretaria_schema import DashboardSecretariaOutput

from app.models.usuario import Usuario

router = APIRouter(prefix="/secretaria", tags=["Secretaria Dashboard"])

@router.get("/dashboard", response_model=DashboardSecretariaOutput)
def listar_candidaturas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_secretaria_logada)):
    
    return SecretariaDashboardService.listar_candidaturas(db)