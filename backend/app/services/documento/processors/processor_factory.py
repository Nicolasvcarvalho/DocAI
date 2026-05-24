from app.services.documento.processors.identificacao_processor import DocumentoIdentificacaoProcessor
from app.services.documento.processors.comprovante_residencia_processor import ComprovanteResidenciaProcessor

class DocumentoProcessorFactory:

    PROCESSORS = {
        "DOCUMENTO_IDENTIFICACAO": DocumentoIdentificacaoProcessor(),
        "COMPROVANTE_RESIDENCIA": ComprovanteResidenciaProcessor(),
    }

    @staticmethod
    def get_processor(tipo_documento_nome: str):

        processor = DocumentoProcessorFactory.PROCESSORS.get(tipo_documento_nome)

        if not processor:

            raise ValueError(f"processor não encontrado para: {tipo_documento_nome}")
        
        return processor