from app.core.database import SessionLocal

from app.repositories.versao_documento_repository import VersaoDocumentoRepository

from app.services.documento.ocr.ocr_service import OCRService
from app.services.documento.workflow.status_workflow import StatusWorkflow

from app.enums.status_documento import StatusDocumento

class OCRTasks:

    @staticmethod
    def processar_documento(versao_documento_id: int):
        
        db = SessionLocal()

        try:

            versao_documento = VersaoDocumentoRepository.buscar_por_id(db=db, versao_documento_id=versao_documento_id)

            if not versao_documento:
                return
            
            StatusWorkflow.transicionar_status(documento=versao_documento.documento, novo_status=StatusDocumento.PROCESSANDO)
            
            db.commit()

            OCRService.executar_ocr_documentos(db=db, versao_documento=versao_documento)
        
        finally:
            
            db.close()