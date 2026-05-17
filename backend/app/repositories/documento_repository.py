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