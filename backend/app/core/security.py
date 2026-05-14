from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def gerar_hash(senha: str):
    return pwd_context.hash(senha)