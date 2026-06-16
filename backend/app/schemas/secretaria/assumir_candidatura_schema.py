from pydantic import BaseModel

from app.enums.status_candidatura import StatusCandidatura

class AssumirCandidaturaResponse(BaseModel):

    id: int
    status: StatusCandidatura
    locked_by_id: int
    mensagem: str