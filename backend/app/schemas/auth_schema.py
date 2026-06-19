from pydantic import BaseModel, EmailStr
from datetime import date
from app.enums.sexo import Sexo
from app.enums.tipo_usuario import TipoUsuario

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

class UsuarioAutenticadoResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    tipo_usuario: TipoUsuario

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    usuario: UsuarioAutenticadoResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str
    