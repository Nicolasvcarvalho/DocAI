from fastapi import Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM

from app.repositories.usuario_repository import UsuarioRepository

from app.models.usuario import Usuario

from app.enums.tipo_usuario import TipoUsuario

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/autenticacao/login_swegger")

def get_usuario_logado(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="token inválido")
    
    usuario = UsuarioRepository.buscar_por_id(db, int(usuario_id))

    if not usuario:

        raise HTTPException(status_code=401, detail="Usuario nao encontrado")
    
    return usuario
    
def get_secretaria_logada(usuario: Usuario = Depends(get_usuario_logado)) -> Usuario:

    if usuario.tipo_usuario != TipoUsuario.SECRETARIA:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para secretarias.")
    
    return usuario

def get_candidato_logado(usuario: Usuario = Depends(get_usuario_logado)) -> Usuario:

    if usuario.tipo_usuario != TipoUsuario.CANDIDATO:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para candidatos.")
    
    return usuario