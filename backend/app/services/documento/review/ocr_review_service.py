from fastapi import HTTPException

from app.repositories.ocr_resultado_repository import OCRResultadoRepository

from app.models.documento import Documento

class OCRReviewService:

    @staticmethod
    def buscar_dados_ocr(db, documento: Documento):

        resultado = OCRResultadoRepository.buscar_por_documento(db=db, documento_id=documento.id)

        if not resultado:
            raise HTTPException(status_code=404, detail="Resultado OCR não encontrado")
        
        return {
            "documento_id": documento.id,
            "tipo_documento": documento.tipo_documento.nome,
            "dados_extraidos": resultado.dados_json
        }