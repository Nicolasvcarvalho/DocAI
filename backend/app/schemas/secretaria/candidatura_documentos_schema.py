from pydantic import BaseModel

class DocumentoResumoOutput(BaseModel):
    id: int
    tipo_documento: str
    status: str

class CandidaturaDocumentosResponse(BaseModel):
    candidatura_id: int
    documentos: list[DocumentoResumoOutput]