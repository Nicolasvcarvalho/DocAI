from pydantic import BaseModel

from app.enums.lado_documento import Lado

class ArquivoDocumentoCreateSchema(BaseModel):

    versao_documento_id: int
    lado: Lado
    file_path: str
    mime_type: str