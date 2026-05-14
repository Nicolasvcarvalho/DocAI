from sqlalchemy import Column, Integer, String, Enum, Date
from app.core.database import Base

from app.enums.tipo_usuario import TipoUsuario

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    tipo_usuario = Column(Enum(TipoUsuario), nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": tipo_usuario
    }


