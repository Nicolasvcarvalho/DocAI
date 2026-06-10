from fastapi import HTTPException

from app.enums.tipo_usuario import TipoUsuario
from app.models.documento import Documento
from app.models.usuario import Usuario

class DocumentoPermission:

    @staticmethod
    def validar_acesso(documento: Documento, usuario: Usuario) -> None:

        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        if usuario.tipo_usuario == TipoUsuario.SECRETARIA:
            return
        
        if usuario.tipo_usuario==TipoUsuario.CANDIDATO and documento.candidatura.candidato_id==usuario.id:
            return
        
        raise HTTPException(status_code=403, detail="Acesso negado ao documento")