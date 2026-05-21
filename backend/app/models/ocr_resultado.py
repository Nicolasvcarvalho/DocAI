from sqlalchemy import Column, Integer, Text, JSON, ForeignKey

from app.core.database import Base

class OCRResultado(Base):

    __tablename__ = "ocr_resultados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    versao_documento_id = Column(Integer, ForeignKey("versoes_documento.id"), nullable=False)
    texto_extraido = Column(Text, nullable=True)
    dados_json = Column(JSON, nullable=True)