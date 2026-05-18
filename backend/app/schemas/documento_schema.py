from pydantic import BaseModel

from app.enums.status_documento import StatusDocumento
from .tipo_documento_schema import TipoDocumentoResponse

class DocumentoResponse(BaseModel):

    id: int
    status: StatusDocumento
    tipo_documento: TipoDocumentoResponse

    class Config:
        from_attributes = True