from app.services.documento.ocr.extractors.rg_extractor import RGExtractor
from app.services.documento.ocr.extractors.comprovante_residencia_extractor import ComprovanteResidenciaExtractor


class OCRExtractorFactory:

    EXTRACTORS = {
        "DOCUMENTO_IDENTIFICACAO": RGExtractor,
        "COMPROVANTE_RESIDENCIA": ComprovanteResidenciaExtractor
    }

    @classmethod
    def obter_extractor(
        cls,
        tipo_documento_nome
    ):

        return cls.EXTRACTORS[
            tipo_documento_nome
        ]