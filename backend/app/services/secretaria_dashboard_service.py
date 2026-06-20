from sqlalchemy.orm import Session

from app.repositories.candidatura_repository import CandidaturaRepository

from app.services.documento.calculators.progresso_documental_calculator import ProgressoDocumentalCalculator
from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService

class SecretariaDashboardService:

    @staticmethod
    def listar_candidaturas(db: Session) -> dict:
        
        candidaturas_disponiveis_para_analise = CandidaturaRepository.listar_disponiveis_para_analise(db)

        total_candidaturas = len(candidaturas_disponiveis_para_analise)
        
        resultado = []

        for candidatura in candidaturas_disponiveis_para_analise:

            status = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)
            progresso = ProgressoDocumentalCalculator.calcular(candidatura)
            possui_reenvio = (progresso.get("reenviados") > 0)

            resultado.append({
                "id": candidatura.id,
                "nome_candidato": f"{candidatura.candidato.nome} {candidatura.candidato.sobrenome}",
                "status": status,
                "possui_reenvio": possui_reenvio,
                "total_documentos": progresso.get("total"),
                "documentos_aprovados": progresso.get("aprovados"),
                "documentos_reenviados": progresso.get("reenviados")             
            })

        return {
            "total_candidaturas": total_candidaturas,
            "candidaturas": resultado
        }

       
            