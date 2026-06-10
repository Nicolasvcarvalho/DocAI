from sqlalchemy.orm import Session

from app.models.documento import Documento
from app.schemas.documento_schema import DocumentoCreateSchema

class DocumentoRepository:
    
    @staticmethod
    def salvar_varios(db: Session, documentos: list[Documento]):

        db.add_all(documentos)
        db.commit()

        for documento in documentos:
            db.refresh(documento)

        return documentos
    
    @staticmethod
    def buscar_por_candidatura(db: Session, candidatura_id):

        return db.query(Documento).filter(Documento.candidatura_id == candidatura_id).all()
    
    @staticmethod
    def buscar_por_candidatura_e_tipo(db, candidatura_id: int, tipo_documento_id: int):
        
        return db.query(Documento).filter(Documento.candidatura_id==candidatura_id, Documento.tipo_documento_id==tipo_documento_id).first()
    
    @staticmethod
    def criar(db, dados: DocumentoCreateSchema):

        documento = Documento(
            status=dados.status,
            candidatura_id=dados.candidatura_id,
            tipo_documento_id=dados.tipo_documento_id
        )

        db.add(documento)

        db.flush()

        return documento
    
    @staticmethod
    def buscar_por_id(db, documento_id: int):

        return db.query(Documento).filter(Documento.id==documento_id).first()