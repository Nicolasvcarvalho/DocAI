from sqlalchemy import Column, Enum, Date

from app.models.usuario import Usuario
from app.enums.sexo import Sexo
from app.enums.tipo_usuario import TipoUsuario 

class Candidato(Usuario):
    
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(Enum(Sexo), nullable=True)

    
    __mapper_args__ = {
        "polymorphic_identity": TipoUsuario.CANDIDATO
    }