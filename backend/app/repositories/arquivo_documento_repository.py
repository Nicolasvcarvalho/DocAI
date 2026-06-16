from app.models.arquivo_documento import ArquivoDocumento

from app.schemas.arquivo_documento_schema import ArquivoDocumentoCreateSchema

class ArquivoDocumentoRepository:

    @staticmethod
    def criar(db, dados: ArquivoDocumentoCreateSchema):
        
        arquivo = ArquivoDocumento(
            versao_documento_id=dados.versao_documento_id,
            lado=dados.lado,
            file_path=dados.file_path, 
            mime_type=dados.mime_type
        )

        db.add(arquivo)

        db.flush()

        return arquivo
    
    @staticmethod
    def buscar_por_id(db, arquivo_id: int):

        return db.query(ArquivoDocumento).filter(ArquivoDocumento.id == arquivo_id).first()