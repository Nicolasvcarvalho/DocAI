from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey

from app.core.database import Base
from app.enums.sexo import Sexo

class TipoDocumento(Base):
     
    __tablename__ = "tipos_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    obrigatorio_base = Column(Boolean, nullable=False, default=True)
    exige_maioridade = Column(Boolean, nullable=False, default=False)
    exige_frente_verso = Column(Boolean, nullable=False, default=False)
    sexo_obrigatorio = Column(Enum(Sexo), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)

    