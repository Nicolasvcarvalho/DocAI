from pydantic import BaseModel
from app.schemas.secretaria.ocr_response import OCRResponse
from app.schemas.secretaria.arquivo_documento_schema import ArquivoDocumentoResponse

class DocumentoAnaliseResponse(BaseModel):

    id: int
    nome_documento: str
    status: str
    possui_reenvio: bool
    total_versoes: int
    ocr: OCRResponse
    arquivos: list[ArquivoDocumentoResponse]