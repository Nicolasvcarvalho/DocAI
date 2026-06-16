from pydantic import BaseModel

from app.enums.lado_documento import Lado

class ArquivoDocumentoResponse(BaseModel):

    id: int
    lado: Lado
    mime_type: str