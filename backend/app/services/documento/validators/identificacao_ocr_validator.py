from app.services.documento.validators.ocr_validator import OCRValidator

class DocumentoIdentificacaoOCRValidator(OCRValidator):

    CAMPOS_OBRIGATORIOS = ["nome", "rg", "cpf", "data_nascimento", "nome_pai", "nome_mae"]