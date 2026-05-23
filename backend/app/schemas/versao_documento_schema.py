from pydantic import BaseModel

class CriarVersaoDocumentoSchema(BaseModel):

    documento_id: int
    versao: int