from sqlalchemy import Column, Enum, Date
from datetime import date

from app.models.usuario import Usuario
from app.enums.sexo import Sexo
from app.enums.tipo_usuario import TipoUsuario 

class Candidato(Usuario):
    
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(Enum(Sexo), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": TipoUsuario.CANDIDATO
    }

    def calcular_idade(self):

        hoje = date.today()

        idade = hoje.year - self.data_nascimento.year

        if (self.data_nascimento.month, self.data_nascimento.day) > (hoje.month, hoje.day):
            idade -= 1

        return idade