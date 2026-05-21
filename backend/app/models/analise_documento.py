from sqlalchemy import Column, Integer, String, Enum, ForeignKey

from app.core.database import Base

class AnaliseDocumento(Base):

    __tablename__ = "analises_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    versao_documento_id = Column(Integer, ForeignKey("versoes_documento.id"), nullable=False)
    secretaria_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(String, nullable=False)
    motivo_rejeicao = Column(String, nullable=True)
    observacao = Column(String, nullable=True)