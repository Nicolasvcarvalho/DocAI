from fastapi import HTTPException
from app.services.secretaria.candidatura_lock_service import CandidaturaLockService

class CandidaturaLockValidator:

    @staticmethod
    def validar(candidatura, secretaria):

        if not candidatura.possui_analista:
            raise HTTPException(status_code=403, detail="Candidatura não foi assumida")

        if candidatura.locked_by_id != secretaria.id:
            raise HTTPException(status_code=403, detail="Candidatura está sob responsabilidade de outra secretaria")
        
        CandidaturaLockService.renovar_lock(candidatura, secretaria)
        
