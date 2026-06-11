from app.models.candidatura import Candidatura

from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService
from app.services.documento.calculators.progresso_documental_calculator import ProgressoDocumentalCalculator
from app.services.documento.permissions.DocumentoActionService import DocumentoPermissionService

class CandidaturaDashboardPresenter:

    @staticmethod
    def montar_dashboard(candidatura: Candidatura) -> dict:

        status_candidatura = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)
        progresso = ProgressoDocumentalCalculator.calcular(candidatura)

        documentos = []
        for documento in candidatura.documentos:
            
            documentos.append({
                "id": documento.id,
                "nome": documento.tipo_documento.nome,
                "status": documento.status,
                "acoes": DocumentoPermissionService.obter_acoes_permitidas(documento)
            })            

        return {
            "status_candidatura": status_candidatura,
            "progresso": progresso,
            "documentos": documentos
        }

