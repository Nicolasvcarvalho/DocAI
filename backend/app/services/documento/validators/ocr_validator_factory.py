from app.services.documento.validators.doc_identificacao_ocr_validator import DocumentoIdentificacaoOCRValidator
from app.services.documento.validators.doc_residencia_ocr_validator import ComprovanteResidenciaOCRValidator

from app.models.tipo_documento import TipoDocumento

class OCRValidatorFactory:

    VALIDATORS = {
        "DOCUMENTO_IDENTIFICACAO": DocumentoIdentificacaoOCRValidator,
        "COMPROVANTE_RESIDENCIA": ComprovanteResidenciaOCRValidator
    }

    @classmethod
    def obter_validator(cls, tipo_documento: TipoDocumento):

        return cls.VALIDATORS.get(tipo_documento.nome)