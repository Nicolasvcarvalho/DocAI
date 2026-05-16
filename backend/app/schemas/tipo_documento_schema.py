from pydantic import BaseModel

class TipoDocumentoResponse(BaseModel):

    id: int
    nome: str

    class Config:
        from_attributes = True