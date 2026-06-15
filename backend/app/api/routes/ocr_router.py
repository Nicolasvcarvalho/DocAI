from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_candidato_logado

from app.repositories.documento_repository import DocumentoRepository

from app.schemas.ocr_review_schema import ConfirmacaoOCRSchema

from app.services.documento.permissions.DocumentoPermission import DocumentoPermission
from app.services.documento.review.ocr_review_service import OCRReviewService
from app.services.documento.validators.ocr_validator_factory import OCRValidatorFactory
from app.services.documento.review.confirmacao_ocr_service import ConfirmacaoOCRService

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.get("/documentos/{documento_id}")
def buscar_dados_ocr(documento_id: int, db: Session = Depends(get_db), usuario=Depends(get_candidato_logado)):

    documento = DocumentoRepository.buscar_por_id(db, documento_id)

    DocumentoPermission.validar_acesso(documento=documento, usuario=usuario)

    return OCRReviewService.buscar_dados_ocr(db=db, documento=documento)

@router.post("/documentos/{documento_id}/confirmar")
def confirmar_ocr(documento_id: int, dados: ConfirmacaoOCRSchema, db: Session = Depends(get_db), usuario=Depends(get_candidato_logado)):

    documento = DocumentoRepository.buscar_por_id(db=db, documento_id=documento_id)

    DocumentoPermission.validar_acesso(documento=documento, usuario=usuario)

    validator = OCRValidatorFactory.obter_validator(documento.tipo_documento)

    validator.validar(dados.dados_corrigidos)

    return ConfirmacaoOCRService.confirmar_ocr(db=db, documento=documento, dados_corrigidos=dados.dados_corrigidos)