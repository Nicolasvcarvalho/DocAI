from sqlalchemy import func

from models.versao_documento import VersaoDocumento

from app.schemas.versao_documento_schema import CriarVersaoDocumentoSchema

class VersaoDocumentoRepository:

    @staticmethod
    def criar(db, dados: CriarVersaoDocumentoSchema):

        versao = VersaoDocumento(dados)

        db.add(versao)

        db.flush()

        return versao
    
    @staticmethod
    def buscar_ultima_versao(db, documento_id: int):

        return db.query(func.max(VersaoDocumento.versao)).filter(VersaoDocumento.id==documento_id).scalar()
    
    