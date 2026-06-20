from app.services.documento.validators.ocr_validator import OCRValidator
from app.services.documento.validators.field_validator import FieldValidator

class DocumentoIdentificacaoOCRValidator(OCRValidator):

    CAMPOS_OBRIGATORIOS = ["nome", "rg", "cpf", "data_nascimento", "nome_pai", "nome_mae"]

    @classmethod
    def validar(cls, dados: dict):
        
        super().validar(dados)

        dados["cpf"] = FieldValidator.validar_cpf(dados["cpf"])

        dados["rg"] = FieldValidator.validar_rg(dados["rg"])

        dados["data_nascimento"] = FieldValidator.validar_data_nascimento(dados["data_nascimento"])

        return dados
    