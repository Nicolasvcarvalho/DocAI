from app.services.documento.validators.ocr_validator import OCRValidator 

class ComprovanteResidenciaOCRValidator(OCRValidator):

    CAMPOS_OBRIGATORIOS = ["logradouro", "numero", "bairro", "cidade", "estado", "cep"]
