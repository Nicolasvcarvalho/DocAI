from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base

class VersaoDocumento(Base):

    __tablename__ = "versoes_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documentos.id"), nullable=False)
    ocr_resultado_id = Column(Integer, ForeignKey("ocr_resultados.id"), nullable=True)
    versao = Column(Integer, nullable=False)

    documento = relationship("Documento", back_populates="versoes")