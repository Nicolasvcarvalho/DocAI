from pydantic import BaseModel, EmailStr
from datetime import date

class CandidatoCreate(BaseModel):
    nome: str
    sobrenome: str
    sexo: str
    data_nascimento: date
    email: EmailStr
    senha: str