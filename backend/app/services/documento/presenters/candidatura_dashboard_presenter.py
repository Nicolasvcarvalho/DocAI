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
                "tipo_documento_id": documento.tipo_documento.id,
                "status": documento.status,
                "aceita_frente_verso": documento.tipo_documento.exige_frente_verso,
                "acoes": DocumentoPermissionService.obter_acoes_permitidas(documento)
            })            

        return {
            "status_candidatura": status_candidatura,
            "progresso": progresso,
            "documentos": documentos
        }

