from pydantic import BaseModel

class CandidaturaResumoOutput(BaseModel):

    id: int
    nome_candidato: str
    status: str
    possui_reenvio: bool
    total_documentos: int
    documentos_aprovados: int
    documentos_reenviados: int

class DashboardSecretariaOutput(BaseModel):

    total_candidaturas: int
    candidaturas: list[CandidaturaResumoOutput]

