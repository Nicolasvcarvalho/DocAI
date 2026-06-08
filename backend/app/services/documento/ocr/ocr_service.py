from app.repositories.ocr_resultado_repository import OCRResultadoRepository

from app.enums.status_documento import StatusDocumento

from app.schemas.ocr_schema import OCRResultadoUpdateSchema
from app.schemas.ocr_schema import OCRResultadoCreateSchema

from app.models.versao_documento import VersaoDocumento

from app.services.documento.workflow.status_workflow import StatusWorkflow

class OCRService:

    @staticmethod
    def executar_ocr_documentos(db, versao_documento: VersaoDocumento):

        texto_extraido = """
        NOME: JOAO TESTE
        CPF: 12345678900
        DATA NASCIMENTO: 01/01/2000
        """

        dados_json = {
            "nome": "JOAO TESTE",
            "cpf": "12345678900",
            "data_nascimento": "2000-01-01"
        }

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

        StatusWorkflow.transicionar_status(documento=versao_documento.documento, novo_status=StatusDocumento.AGUARDANDO_CONFIRMACAO)

        db.commit()