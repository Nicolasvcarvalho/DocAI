from pydantic import BaseModel

from app.enums.status_documento import StatusDocumento
from app.enums.status_candidatura import StatusCandidatura

class DocumentoAcoesResponse(BaseModel):

    pode_visualizar_arquivo: bool
    pode_enviar_documento: bool
    pode_reenviar_documento: bool
    pode_confirmar_ocr: bool
    pode_editar_dados_ocr: bool

class DocumentoDashboardResponse(BaseModel):

    id: int
    nome: str
    status: StatusDocumento
    acoes: DocumentoAcoesResponse

class ProgressoDocumentalResponse(BaseModel):

    total: int
    enviados: int
    aprovados: int
    rejeitados: int
    percentual: int

class CandidaturaDashboardResponse(BaseModel):

    status_candidatura: StatusCandidatura
    progresso: ProgressoDocumentalResponse
    documentos: list[DocumentoDashboardResponse]
