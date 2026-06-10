from typing import Dict, Any

from pydantic import BaseModel

class OCRDadosResponse(BaseModel):

    documento_id: int
    tipo_documento: str
    dados_extraidos: dict


class ConfirmacaoOCRSchema(BaseModel):

    dados_corrigidos: Dict[str, Any]