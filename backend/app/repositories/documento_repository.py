from sqlalchemy.orm import Session

from app.models.documento import Documento

class DocumentoRepository:
    
    @staticmethod
    def salvar_varios(db: Session, documentos: list[Documento]):

        db.add_all(documentos)
        db.commit()

        for documento in documentos:
            db.refresh(documento)

        return documentos
    
    @staticmethod
    def buscar_por_candidatura(db, candidatura_id):

        return db.query(Documento).filter(Documento.candidatura_id == candidatura_id).all()