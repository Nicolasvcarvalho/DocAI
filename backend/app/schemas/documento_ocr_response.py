from pydantic import BaseModel

class OCRDadosResponse(BaseModel):

    documento_id: int
    tipo_documento: str
    dados_extraidos: dict

    