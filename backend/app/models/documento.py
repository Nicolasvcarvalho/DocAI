from sqlalchemy import Column, Integer, Enum, ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.status_documento import StatusDocumento


class Documento(Base):

    __tablename__ = "documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(StatusDocumento), nullable=False)
    candidatura_id = Column(ForeignKey("candidaturas.id"), nullable=False)
    tipo_documento_id = Column(ForeignKey("tipos_documento.id"), nullable=False)

    candidatura = relationship("Candidatura", back_populates="documentos")