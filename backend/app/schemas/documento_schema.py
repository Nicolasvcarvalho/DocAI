from pydantic import BaseModel

from typing import Optional

from app.enums.status_documento import StatusDocumento
from .tipo_documento_schema import TipoDocumentoResponse

class DocumentoResponse(BaseModel):

    id: int
    status: StatusDocumento
    tipo_documento: TipoDocumentoResponse
    versao_atual_id: Optional[int] = None

    class Config:
        from_attributes = True

class DocumentoCreateSchema(BaseModel):

    status: StatusDocumento
    candidatura_id: int
    tipo_documento_id: int

