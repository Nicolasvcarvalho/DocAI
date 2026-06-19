from app.enums.status_documento import StatusDocumento

from app.services.documento.workflow.documento_status_workflow import DocumentoStatusWorkflow
from app.services.documento.review.ocr_review_service import OCRReviewService

from app.models.documento import Documento

from sqlalchemy.orm import Session

class ConfirmacaoOCRService:

    @staticmethod
    def confirmar_ocr(db: Session, documento: Documento, dados_corrigidos: dict):

        OCRReviewService.atualizar_dados_ocr(db=db, documento=documento, dados_corrigidos=dados_corrigidos)

        DocumentoStatusWorkflow.transicionar_status_documento(documento=documento, novo_status=StatusDocumento.EM_ANALISE)

        db.commit()

        return {
            "mensagem": "Dados OCR confirmados com sucesso"
        }