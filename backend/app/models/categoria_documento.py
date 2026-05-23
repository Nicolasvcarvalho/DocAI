from sqlalchemy import Column, Integer, String

from app.core.database import Base

class CategoriaDocumento(Base):
    
    __tablename__ = "categorias_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)