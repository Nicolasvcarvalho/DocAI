from abc import ABC, abstractmethod

from app.schemas.upload_documento_schema import DocumentoUploadInput

from sqlalchemy.orm import Session

class DocumentoProcessor(ABC):

    @abstractmethod
    def processar_upload(self, db: Session, documento, versao_documento, arquivos: DocumentoUploadInput):
        pass