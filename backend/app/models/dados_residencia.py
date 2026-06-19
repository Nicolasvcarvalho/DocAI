from sqlalchemy import Column, Integer, ForeignKey, String

from sqlalchemy.orm import relationship

from app.core.database import Base

class DadosResidencia(Base):

    __tablename__ = "dados_residencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidatura_id = Column(ForeignKey("candidaturas.id"), nullable=False, unique=True)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False)

    candidatura = relationship("Candidatura", back_populates="dados_residencia")