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

        todos_aprovados = all(documento.status==StatusDocumento.APROVADO for documento in documentos_obrigatorios)
        algum_em_analise = any(documento.status==StatusDocumento.EM_ANALISE for documento in documentos_obrigatorios)
        algum_processando = any(
            documento.status in [StatusDocumento.ENVIADO, StatusDocumento.PROCESSANDO, StatusDocumento.AGUARDANDO_CONFIRMACAO]
            for documento in documentos_obrigatorios
            )
        algum_rejeitado = any(documento.status==StatusDocumento.REJEITADO for documento in documentos_obrigatorios)
        algum_pendente_envio = any(documento.status==StatusDocumento.PENDENTE_ENVIO for documento in documentos_obrigatorios)
        
        if algum_pendente_envio:
            return StatusCandidatura.AGUARDANDO_DOCUMENTOS
        
        if algum_processando:
            return StatusCandidatura.DOCUMENTACAO_EM_PROCESSAMENTO
        
        if algum_em_analise:
            return StatusCandidatura.EM_ANALISE
        
        if algum_rejeitado:
            return StatusCandidatura.DOCUMENTACAO_PENDENTE
        
        if todos_aprovados:
            return StatusCandidatura.APROVADA
        
        return StatusCandidatura.DOCUMENTACAO_PENDENTE