from app.services.secretaria.candidatura_lock_service import CandidaturaLockService
from app.services.secretaria.validators.candidatura_lock_validator import CandidaturaLockValidator

class LockGuardService:

    @staticmethod
    def validar_e_renovar(db, candidatura, secretaria):

        CandidaturaLockService.liberar_se_expirado(candidatura)

        CandidaturaLockValidator.validar(candidatura, secretaria)

        CandidaturaLockService.renovar_lock(candidatura, secretaria)

        db.commit()