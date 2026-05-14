from enum import Enum

class TipoUsuario(str, Enum):
    CANDIDATO = "CANDIDATO"
    SECRETARIA = "SECRETARIA"