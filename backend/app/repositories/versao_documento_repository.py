from sqlalchemy import func

from app.models.versao_documento import VersaoDocumento

from app.schemas.versao_documento_schema import VersaoDocumentoCreateSchema

class VersaoDocumentoRepository:

    @staticmethod
    def criar(db, dados: VersaoDocumentoCreateSchema):

        versao = VersaoDocumento(**dados.model_dump())

        db.add(versao)

        db.flush()

        return versao
    
    @staticmethod
    def buscar_ultima_versao(db, documento_id: int):

        return db.query(func.max(VersaoDocumento.versao)).filter(VersaoDocumento.id==documento_id).scalar()
    
