from app.models.analise_documento import AnaliseDocumento

class AnaliseDocumentoRepository:

    @staticmethod
    def criar(db, dados):

        analise = AnaliseDocumento(
            versao_documento_id=dados.versao_documento_id,
            secretaria_id=dados.secretaria_id,
            status=dados.status,
            motivo=dados.motivo
        )

        db.add(analise)

        db.flush()

        return analise