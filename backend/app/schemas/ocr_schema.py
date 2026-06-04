from pydantic import BaseModel

from typing import Optional

class OCRResultadoBaseSchema(BaseModel):

    texto_extraido: Optional[str] = None
    dados_json: Optional[dict] = None

class OCRResultadoCreateSchema(OCRResultadoBaseSchema):

    versao_documento_id: int


class OCRResultadoUpdateSchema(OCRResultadoBaseSchema):

    pass

class OCRResultadoResponseSchema(OCRResultadoBaseSchema):

    id: int
    versao_documento_id: int

    class Config:
        from_attributes = True