from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from sqlalchemy.orm import relationship

from app.enums.lado_documento import Lado

from app.core.database import Base

class ArquivoDocumento(Base):

    __tablename__ = "arquivos_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    versao_documento_id = Column(Integer, ForeignKey("versoes_documento.id"), nullable=False)
    lado = Column(Enum(Lado), nullable=False)
    file_path = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)

    versao_documento = relationship("VersaoDocumento", back_populates="arquivos")