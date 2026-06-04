from sqlalchemy import Column, Integer, Text, JSON, ForeignKey

from app.core.database import Base

from sqlalchemy.orm import relationship

class OCRResultado(Base):

    __tablename__ = "ocr_resultados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    versao_documento_id = Column(Integer, ForeignKey("versoes_documento.id"), nullable=False)
    texto_extraido = Column(Text, nullable=True)
    dados_json = Column(JSON, nullable=True)

    versao_documento = relationship("VersaoDocumento", back_populates="ocr_resultado")