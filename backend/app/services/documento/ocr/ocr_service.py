from app.repositories.ocr_resultado_repository import OCRResultadoRepository

from app.enums.status_documento import StatusDocumento

from app.schemas.ocr_schema import OCRResultadoUpdateSchema
from app.schemas.ocr_schema import OCRResultadoCreateSchema

from app.models.versao_documento import VersaoDocumento

from app.services.documento.workflow.documento_status_workflow import DocumentoStatusWorkflow
from app.services.documento.ocr.ocr_extractor_factory import OCRExtractorFactory

class OCRService:

    @staticmethod
    def executar_ocr_documentos(db, versao_documento: VersaoDocumento):

        extractor = OCRExtractorFactory.obter_extractor(versao_documento.documento.tipo_documento.nome)

        dados_json, texto_extraido = extractor.executar(versao_documento)

        resultado_existente = OCRResultadoRepository.buscar_por_versao(db, versao_documento_id=versao_documento.id)

        if resultado_existente:

            schema_update_ocr_resultado = OCRResultadoUpdateSchema(texto_extraido=texto_extraido, dados_json=dados_json)
            OCRResultadoRepository.atualizar_dados(resultado=resultado_existente, dados=schema_update_ocr_resultado)

        else:

            schema_create_ocr_resultado = OCRResultadoCreateSchema(
                versao_documento_id=versao_documento.id,
                texto_extraido=texto_extraido,
                dados_json=dados_json
                )
            OCRResultadoRepository.criar(db=db, dados=schema_create_ocr_resultado)

        DocumentoStatusWorkflow.transicionar_status_documento(db=db, documento=versao_documento.documento, novo_status=StatusDocumento.AGUARDANDO_CONFIRMACAO)

        db.commit()