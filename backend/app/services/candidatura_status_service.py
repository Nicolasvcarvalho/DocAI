from sqlalchemy.orm import Session

from app.models.candidatura import Candidatura

from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService

class CandidaturaStatusService:

    @staticmethod
    def sincronizar(candidatura: Candidatura):

        novo_status = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)

        candidatura.status = novo_status

        return candidatura