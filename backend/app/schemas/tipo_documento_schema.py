from pydantic import BaseModel

from typing import Optional

class TipoDocumentoResponse(BaseModel):

    id: int
    nome: str
    exige_frente_verso: Optional[bool] = None

    class Config:
        from_attributes = True