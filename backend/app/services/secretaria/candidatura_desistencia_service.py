from fastapi import HTTPException

from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService
from app.services.secretaria.validators.candidatura_lock_validator import CandidaturaLockValidator

from app.repositories.candidatura_repository import CandidaturaRepository

from app.enums.status_candidatura import StatusCandidatura

from app.schemas.secretaria.desistir_analise_schema import DesistirAnaliseResponse

class CandidaturaDesistenciaService:

    @staticmethod
    def desistir(db, candidatura, secretaria):

        CandidaturaLockValidator.validar(candidatura, secretaria)

        if candidatura.status == StatusCandidatura.APROVADA:
            raise HTTPException(status_code=409, detail="A candidatura já foi aprovada")

        CandidaturaRepository.liberar_lock(candidatura)

        candidatura.status = CandidaturaWorkflowService.recalcular_stasttus_candidatura(candidatura)

        db.commit()

        db.refresh()

        return DesistirAnaliseResponse(
            candidatura_id=candidatura.id,
            status_candidatura=candidatura.status,
            mensagem="Análise abandonada com sucesso"
        )