from app.models.arquivo_documento import ArquivoDocumento

from app.schemas.arquivo_documento_schema import ArquivoDocumentoCreateSchema

class ArquivoDocumentoRepository:

    @staticmethod
    def criar(db, dados: ArquivoDocumentoCreateSchema):
        
        arquivo = ArquivoDocumento(
            versao_documento_id=dados.versao_documento_id,
            lado=dados.lado,
            file_path=dados.file_path
        )

        db.add(arquivo)

        db.flush()

        return arquivo