from pydantic import BaseModel, EmailStr
from datetime import date

from .tipo_documento_schema import TipoDocumentoResponse

class CandidatoCreate(BaseModel):
    nome: str
    sobrenome: str
    sexo: str
    data_nascimento: date
    email: EmailStr
    senha: str

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    tipo_usuario: str
    candidatura_id: int | None = None
    documentos_obrigatorios: list[TipoDocumentoResponse]