from fastapi import HTTPException

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

SECRET_KEY = "sfjkdlflsadfndjs"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

REFRESH_TOKEN_EXPIRE_DAYS = 7

def gerar_hash(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)

def criar_access_token(data: dict):

    dados = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dados.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def criar_refresh_token(data: dict):

    dados = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    dados.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decodificar_token(token: str):

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expirado")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="token inválido")
    
def validar_tipo_token(payload: dict, tipo_esperado: str):

    tipo = payload.get("type")

    if tipo != tipo_esperado:
        raise HTTPException(status_code=401, detail=f"{tipo_esperado.capitalize()} token inválido")