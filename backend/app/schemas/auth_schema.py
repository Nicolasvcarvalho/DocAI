from pydantic import BaseModel, EmailStr
from datetime import date
from app.enums.sexo import Sexo

from .documento_schema import DocumentoResponse

class CandidatoCreate(BaseModel):
    nome: str
    sobrenome: str
    sexo: Sexo
    data_nascimento: date
    email: EmailStr
    senha: str

class CandidatoCreateResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: EmailStr
    tipo_usuario: str
    mensagem: str

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    tipo_usuario: str
    candidatura_id: int | None = None
    documentos_obrigatorios: list[DocumentoResponse]