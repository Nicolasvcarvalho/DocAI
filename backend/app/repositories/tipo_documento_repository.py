from app.models.tipo_documento import TipoDocumento

class TipoDocumentoRepository:

    @staticmethod
    def buscar_ativos(db):
        return db.query(TipoDocumento).filter(TipoDocumento.ativo==True).all()