from models.versao_documento import VersaoDocumento

from app.schemas.versao_documento_schema import CriarVersaoDocumentoSchema

class VersaoDocumentoRepository:

    @staticmethod
    def criar(db, dados: CriarVersaoDocumentoSchema):

        versao = VersaoDocumento(dados)

        db.add(versao)

        db.flush()

        return versao