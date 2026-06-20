from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.enums.status_analise import StatusAnalise
from app.core.database import Base

class AnaliseDocumento(Base):

    __tablename__ = "analises_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    versao_documento_id = Column(Integer, ForeignKey("versoes_documento.id"), nullable=False)
    secretaria_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(Enum(StatusAnalise), nullable=False)
    motivo = Column(String, nullable=True)

    versao_documento = relationship("VersaoDocumento", back_populates="analise")