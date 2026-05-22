from models.versao_documento import VersaoDocumento

class VersaoDocumentoRepository:

    @staticmethod
    def criar(db, dados):

        versao = VersaoDocumento(**dados)

        db.add(versao)

        db.flush()

        return versao