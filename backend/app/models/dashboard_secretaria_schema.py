from pydantic import BaseModel

class CandidaturaResumoOutput(BaseModel):

    id: int
    nome_candidato: str
    status: str
    total_documentos: int
    documentos_aprovados: int
    documentos_pendentes: int
    possui_rejeicao: bool

class DashboardSecretariaOutput(BaseModel):

    total_candidaturas: int
    em_analise: int
    pendentes: int
    aprovados: int
    candidaturas: list[CandidaturaResumoOutput]

