from pydantic import BaseModel

class DadosResidenciaCreateSchema(BaseModel):

    candidatura_id: int
    logradouro: str
    numero: str 
    bairro: str 
    cidade: str
    estado: str
    cep: str