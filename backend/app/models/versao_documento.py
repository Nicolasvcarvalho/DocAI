from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base

class VersaoDocumento(Base):

    __tablename__ = "versoes_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documento.id"), nullable=False)
    versao = Column(Integer, nullable=False)

    documento = relationship("Documento", back_populates="versoes", foreign_keys=[documento_id])
    arquivos = relationship("ArquivoDocumento", back_populates="versao_documento")
    ocr_resultado = relationship("OCRResultado", back_populates="versao_documento", uselist=False)