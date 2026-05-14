from sqlalchemy import Column, String

from app.models.usuario import Usuario
from app.enums.tipo_usuario import TipoUsuario

class Secretaria(Usuario):

    cpf = Column(String(11), unique=True, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": TipoUsuario.SECRETARIA
    }