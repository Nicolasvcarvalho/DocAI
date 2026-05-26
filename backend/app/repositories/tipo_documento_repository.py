from app.models.tipo_documento import TipoDocumento

class TipoDocumentoRepository:

    @staticmethod
    def buscar_ativos(db):
        return db.query(TipoDocumento).filter(TipoDocumento.ativo==True).all()
    
    @staticmethod
    def buscar_por_id(db, tipo_documento_id: int):
        return db.query(TipoDocumento).filter(TipoDocumento.id==tipo_documento_id).first()