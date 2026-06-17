from app.repositories.candidatura_repository import CandidaturaRepository

from app.enums.status_candidatura import StatusCandidatura

from app.services.secretaria.validators.candidatura_assumir_validator import CandidaturaAssumirValidator
from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService

from datetime import datetime, UTC, timedelta

class CandidaturaLockService:

    @staticmethod
    def assumir(db, candidatura, secretaria):

        CandidaturaLockService.liberar_se_expirado(candidatura)

        CandidaturaAssumirValidator.validar(candidatura)

        CandidaturaRepository.assumir(
            candidatura=candidatura,
            secretaria_id=secretaria.id
        )

        novo_status = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)
        candidatura.status = novo_status

        db.commit()

        db.refresh(candidatura)

        return candidatura
    
    @staticmethod
    def liberar_se_expirado(candidatura):

        if not candidatura.lock_expires_at:
            return

        agora = datetime.now(UTC)

        if candidatura.lock_expires_at > agora:
            return

        CandidaturaRepository.liberar_lock(candidatura)

    @staticmethod
    def renovar_lock(candidatura, secretaria):

        if candidatura.locked_by_id!= secretaria.id:
            return
    
        candidatura.lock_expires_at = datetime.now(UTC) + timedelta(minutes=30)

    @staticmethod
    def finalizar_se_necessario(candidatura):

        if candidatura.status in [
            StatusCandidatura.APROVADA,
            StatusCandidatura.AGUARDANDO_DOCUMENTOS,
            StatusCandidatura.DOCUMENTACAO_PENDENTE
        ]:

            CandidaturaRepository.liberar_lock(candidatura)