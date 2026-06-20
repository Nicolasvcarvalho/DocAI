from pydantic import BaseModel

from app.enums.status_candidatura import StatusCandidatura

class DesistirAnaliseResponse(BaseModel):

    candidatura_id: int
    status_candidatura: StatusCandidatura
    mensagem: str