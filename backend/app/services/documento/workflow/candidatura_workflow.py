from app.models.candidatura import Candidatura

from app.enums.status_candidatura import StatusCandidatura
from app.enums.status_documento import StatusDocumento

class CandidaturaWorkflowService:

    @staticmethod
    def recalcular_status_candidatura(candidatura: Candidatura) -> StatusCandidatura:

        documentos = candidatura.documentos

        if not documentos:
            return StatusCandidatura.AGUARDANDO_DOCUMENTOS

        documentos_obrigatorios = [
            documento
            for documento in documentos
            if documento.tipo_documento.obrigatorio_base
        ]

        status_presentes = {documento.status for documento in documentos_obrigatorios}

        if StatusDocumento.PENDENTE_ENVIO in status_presentes:
            return StatusCandidatura.AGUARDANDO_DOCUMENTOS

        status_processamento = {
            StatusDocumento.ENVIADO,
            StatusDocumento.PROCESSANDO,
            StatusDocumento.AGUARDANDO_CONFIRMACAO
        }

        if status_presentes.intersection(status_processamento):
            return StatusCandidatura.DOCUMENTACAO_EM_PROCESSAMENTO

        if StatusDocumento.EM_ANALISE in status_presentes:
            return StatusCandidatura.EM_ANALISE if candidatura.possui_analista else StatusCandidatura.DOCUMENTACAO_PENDENTE

        if status_presentes == {StatusDocumento.APROVADO}:
            return StatusCandidatura.APROVADA

        status_finais = {
            StatusDocumento.APROVADO,
            StatusDocumento.AGUARDANDO_REENVIO
        }

        if status_presentes.issubset(status_finais):
            return StatusCandidatura.CORRECAO_SOLICITADA

        raise ValueError(f"Status de documentos não mapeado: {status_presentes}")