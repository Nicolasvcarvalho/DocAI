from app.enums.status_analise import StatusAnalise

from pydantic import BaseModel

class SolicitarCorrecaoInput(BaseModel):

    motivo: str


class AnaliseDocumentoResponse(BaseModel):

    documento_id: int
    status_documento: str
    status_candidatura: str
    mensagem: str

    class Config:
        from_attributes = True

class AnaliseDocumentoCreateSchema(BaseModel):

    versao_documento_id: int
    secretaria_id: int
    status: StatusAnalise
    motivo: str | None = None