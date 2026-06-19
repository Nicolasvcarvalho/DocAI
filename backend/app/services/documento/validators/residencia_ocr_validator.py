from app.services.documento.validators.field_validator import FieldValidator
from app.services.documento.validators.ocr_validator import OCRValidator 

class ComprovanteResidenciaOCRValidator(OCRValidator):

    CAMPOS_OBRIGATORIOS = ["logradouro", "numero", "bairro", "cidade", "estado", "cep"]

    @classmethod
    def validar(cls, dados: dict):

        super().validar(dados)

        dados["cep"] = FieldValidator.validar_cep(dados["cep"])
        
        dados["estado"] = FieldValidator.validar_uf(dados["estado"])

        return dados