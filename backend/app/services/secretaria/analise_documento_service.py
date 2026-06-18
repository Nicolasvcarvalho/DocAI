from app.enums.status_documento import StatusDocumento
from app.enums.status_analise import StatusAnalise

from app.schemas.secretaria.analise_documento_schema import AnaliseDocumentoCreateSchema
from app.schemas.secretaria.analise_documento_schema import AnaliseDocumentoResponse

from app.repositories.analise_documento_repository import AnaliseDocumentoRepository

from app.services.documento.workflow.documento_status_workflow import DocumentoStatusWorkflow
from app.services.documento.workflow.candidatura_workflow import CandidaturaWorkflowService
from app.services.secretaria.candidatura_lock_service import CandidaturaLockService
from app.services.secretaria.validators.candidatura_lock_validator import CandidaturaLockValidator

class AnaliseDocumentoService:

    @staticmethod
    def aprovar(db, documento, secretaria):

        candidatura = documento.candidatura       

        dados = AnaliseDocumentoCreateSchema(
            versao_documento_id=documento.versao_atual_id,
            secretaria_id=secretaria.id,
            status=StatusAnalise.APROVADO
        )
    
        AnaliseDocumentoRepository.criar(db, dados)

        DocumentoStatusWorkflow.transicionar_status_documento(
            db=db,
            documento=documento,
            novo_status=StatusDocumento.APROVADO
        )
            
        novo_status = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)
        
        candidatura.status = novo_status

        CandidaturaLockService.finalizar_se_necessario(candidatura)

        db.commit()

        db.refresh(documento)

        return AnaliseDocumentoResponse(
            documento_id=documento.id,
            status_documento=documento.status,
            status_candidatura=candidatura.status,
            mensagem="Documento aprovado com sucesso"
        )
    
    @staticmethod
    def solicitar_correcao(db, documento, secretaria, motivo):

        candidatura = documento.candidatura

        dados = AnaliseDocumentoCreateSchema(
            versao_documento_id=documento.versao_atual_id,
            secretaria_id=secretaria.id,
            status=StatusAnalise.REPROVADO,
            motivo=motivo
        )
        
        AnaliseDocumentoRepository.criar(db, dados)

        DocumentoStatusWorkflow.transicionar_status_documento(
            db=db,
            documento=documento,
            novo_status=StatusDocumento.AGUARDANDO_REENVIO
        )

        novo_status = CandidaturaWorkflowService.recalcular_status_candidatura(candidatura)

        candidatura.status = novo_status

        CandidaturaLockService.finalizar_se_necessario(candidatura)

        db.commit()

        db.refresh(documento)

        return AnaliseDocumentoResponse(
            documento_id=documento.id,
            status_documento=documento.status,
            status_candidatura=candidatura.status,
            mensagem="Correção solicitada com sucesso"
        )