from pydantic import BaseModel

from app.enums.lado import Lado

class CriarArquivoDocumentoSchema(BaseModel):

    versao_documento_id: int
    lado: Lado
    file_path: str