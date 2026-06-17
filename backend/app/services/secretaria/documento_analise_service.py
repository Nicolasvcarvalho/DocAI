from app.schemas.secretaria.documento_analise_response import DocumentoAnaliseResponse
from app.schemas.secretaria.ocr_response import OCRResponse
from app.schemas.secretaria.arquivo_documento_schema import ArquivoDocumentoResponse

class DocumentoAnaliseService:

    @staticmethod
    def obter_documento_para_analise(documento):

        versao = documento.versao_atual

        ocr = versao.ocr_resultado

        return DocumentoAnaliseResponse(

            id=documento.id,
            nome_documento=(documento.tipo_documento.nome),
            status=documento.status,
            possui_reenvio=len(documento.versoes) > 1,
            total_versoes=len(documento.versoes),
            ocr=OCRResponse(dados_json=ocr.dados_json),
            arquivos=[
                ArquivoDocumentoResponse(
                    id=arquivo.id,
                    lado=arquivo.lado,
                    mime_type=arquivo.mime_type
                )
                for arquivo in versao.arquivos
            ]
        )