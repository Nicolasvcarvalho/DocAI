from sqlalchemy import Column, Integer, ForeignKey, String, Date

from sqlalchemy.orm import relationship

from app.core.database import Base

class DadosIdentificacao(Base):

    __tablename__ = "dados_identificacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidatura_id = Column(ForeignKey("candidaturas.id"), nullable=False, unique=True)
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False)
    rg = Column(String(30), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    nome_pai = Column(String(255), nullable=False)
    nome_mae = Column(String(255), nullable=False)

    candidatura = relationship("Candidatura", back_populates="dados_identificacao")