from datetime import date

from pydantic import BaseModel


class DadosIdentificacaoCreateSchema(BaseModel):

    candidatura_id: int
    nome_completo: str
    cpf: str
    rg: str 
    data_nascimento: date
    nome_pai: str 
    nome_mae: str 