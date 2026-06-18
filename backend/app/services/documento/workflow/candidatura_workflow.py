from app.models.candidatura import Candidatura

from app.enums.status_candidatura import StatusCandidatura
from app.enums.status_documento import StatusDocumento

class CandidaturaWorkflowService:

    @staticmethod
    def recalcular_status_candidatura(candidatura: Candidatura) -> StatusCandidatura:
            
            documentos = candidatura.documentos

            if not documentos:
                
                return StatusCandidatura.AGUARDANDO_DOCUMENTOS
            
            documentos_obrigatorios = [documento for documento in documentos if documento.tipo_documento.obrigatorio_base]

            status_presentes = {documento.status for documento in documentos_obrigatorios}

            status_esperando_candidato = {StatusDocumento.PENDENTE_ENVIO, StatusDocumento.AGUARDANDO_REENVIO}

            if status_presentes.intersection(status_esperando_candidato):
                return StatusCandidatura.AGUARDANDO_DOCUMENTOS
            
            status_processamento = {StatusDocumento.ENVIADO, StatusDocumento.PROCESSANDO, StatusDocumento.AGUARDANDO_CONFIRMACAO}

            if status_presentes.intersection(status_processamento):
                return StatusCandidatura.DOCUMENTACAO_EM_PROCESSAMENTO
            
            if StatusDocumento.EM_ANALISE in status_presentes:
                return StatusCandidatura.EM_ANALISE if candidatura.possui_analista else StatusCandidatura.DOCUMENTACAO_PENDENTE
            
            if status_presentes == {StatusDocumento.APROVADO}:
                return StatusCandidatura.APROVADA
            
            if StatusDocumento.APROVADO in status_presentes:
                return StatusCandidatura.EM_ANALISE

            raise ValueError(f"Status de documentos não mapeado: {status_presentes}")