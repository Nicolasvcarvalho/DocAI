from fastapi import HTTPException

from app.models.candidato import Candidato
from app.models.candidatura import Candidatura

from app.enums.status_candidatura import StatusCandidatura
from app.enums.tipo_usuario import TipoUsuario

from app.core.security import gerar_hash, verificar_senha, criar_access_token, criar_refresh_token, decodificar_token, validar_tipo_token

from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.documento_repository import DocumentoRepository

from app.services.documento.documento_service import DocumentoService

from app.schemas.auth_schema import UsuarioAutenticadoResponse

class AuthService:

    @staticmethod
    def criar_candidato(db, dados):

        if UsuarioRepository.buscar_email(db, dados.email):
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        senha_hash = gerar_hash(dados.senha)

        candidato = Candidato(
            nome=dados.nome,
            sobrenome=dados.sobrenome,
            data_nascimento=dados.data_nascimento,
            sexo=dados.sexo,
            email=dados.email,
            senha_hash=senha_hash,
            
        )

        UsuarioRepository.salvar_candidato(db, candidato)

        candidatura = Candidatura(
            status=StatusCandidatura.AGUARDANDO_DOCUMENTOS,
            candidato_id=candidato.id
            )
        
        CandidaturaRepository.salvar_candidatura(db, candidatura)

        documentos_iniciais = DocumentoService.criar_documentos_iniciais(db, candidatura, candidato)

        DocumentoRepository.salvar_varios(db, documentos_iniciais)

        return {
            "id": candidato.id,
            "nome": candidato.nome,
            "sobrenome": candidato.sobrenome,
            "email": candidato.email,
            "tipo_usuario": TipoUsuario.CANDIDATO,
            "mensagem": "Candidato criado com sucesso"
        }

    @staticmethod
    def login(db, dados):

        usuario = UsuarioRepository.buscar_email(db, dados.email)

        if not usuario:
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")
        
        senha_valida = verificar_senha(dados.senha, usuario.senha_hash)

        if not senha_valida:
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")
        
        payload = {
            "sub": str(usuario.id),
            "tipo_usuario": usuario.tipo_usuario.value
        }

        access_token = criar_access_token(payload)
        refresh_token = criar_refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "usuario": UsuarioAutenticadoResponse(
                id=usuario.id,
                nome=usuario.nome,
                sobrenome=usuario.sobrenome,
                tipo_usuario=usuario.tipo_usuario
            )
        }
    
    @staticmethod
    def refresh(refresh_token: str):

        payload = decodificar_token(refresh_token)

        validar_tipo_token(payload, "refresh")
            
        novo_access_token = criar_access_token({
            "sub": payload["sub"],
            "tipo_usuario": payload["tipo_usuario"]
        })

        return {
            "access_token": novo_access_token,
            "token_type": "bearer"
        }
        