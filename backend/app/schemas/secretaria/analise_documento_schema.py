from app.enums.status_analise import StatusAnalise
from app.enums.status_candidatura import StatusCandidatura
from app.enums.status_documento import StatusDocumento

from pydantic import BaseModel

class SolicitarCorrecaoInput(BaseModel):

    motivo: str


class AnaliseDocumentoResponse(BaseModel):

    documento_id: int
    status_documento: StatusDocumento
    status_candidatura: StatusCandidatura
    mensagem: str

    class Config:
        from_attributes = True

class AnaliseDocumentoCreateSchema(BaseModel):

    versao_documento_id: int
    secretaria_id: int
    status: StatusAnalise
    motivo: str | None = None