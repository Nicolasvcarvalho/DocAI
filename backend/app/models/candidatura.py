from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime

from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.status_candidatura import StatusCandidatura

class Candidatura(Base):

    __tablename__="candidaturas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(StatusCandidatura), nullable=False)
    candidato_id = Column(ForeignKey("usuarios.id"), nullable=False)
    locked_by_id = Column(ForeignKey("usuarios.id"), nullable=True)
    locked_at = Column(DateTime, nullable=True)
    lock_expires_at = Column(DateTime, nullable=True)

    candidato = relationship("Candidato", foreign_keys=[candidato_id])
    locked_by = relationship("Secretaria", foreign_keys=[locked_by_id])
    documentos = relationship("Documento", back_populates="candidatura")

    @property
    def possui_analista(self):
        return self.locked_by_id is not None
    
    @property
    def esta_disponivel(self):
        return not self.possui_analista and self.status==StatusCandidatura.DOCUMENTACAO_PENDENTE