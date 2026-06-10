from app.models.ocr_resultado import OCRResultado
from app.models.versao_documento import VersaoDocumento

from app.schemas.ocr_schema import OCRResultadoCreateSchema, OCRResultadoUpdateSchema

class OCRResultadoRepository:

    @staticmethod
    def criar(db, dados: OCRResultadoCreateSchema):
        
        resultado = OCRResultado(**dados.model_dump())
        db.add(resultado)
        db.flush()

        return resultado
    
    @staticmethod
    def buscar_por_versao(db, versao_documento_id: int):

        return db.query(OCRResultado).filter(OCRResultado.versao_documento_id==versao_documento_id).first()
    
    @staticmethod
    def atualizar_dados(resultado: OCRResultado, dados: OCRResultadoUpdateSchema):

        resultado.texto_extraido = dados.texto_extraido
        resultado.dados_json = dados.dados_json

        return resultado
    
    @staticmethod
    def buscar_por_documento(db, documento_id: int):

        return db.query(OCRResultado).join(VersaoDocumento).filter(VersaoDocumento.documento_id==documento_id).first()
    