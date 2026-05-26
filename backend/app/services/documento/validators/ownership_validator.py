from fastapi import HTTPException

from app.models.usuario import Usuario
from app.models.documento import Documento
from app.models.candidatura import Candidatura

class OwnershipValidator:

    @staticmethod
    def validar_candidatura_usuario(usuario: Usuario, candidatura: Candidatura):
        
        if candidatura.candidato_id != usuario.id:
            raise HTTPException(status_code=403, detail="Você não possui acesso a esta candidatura")
    
    @staticmethod
    def validar_documento_candidatura(documento: Documento, candidatura: Candidatura):

        if documento.candidatura_id != candidatura.id:
            raise HTTPException(status_code=403, detail="Documento não pertence à esta candidatura")
