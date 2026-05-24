from pydantic import BaseModel

class VersaoDocumentoCreateSchema(BaseModel):

    documento_id: int
    versao: int