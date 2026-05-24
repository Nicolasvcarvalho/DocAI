from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

class DocumentoProcessor(ABC):

    @abstractmethod
    def processar_upload(self, db: Session, documento, versao_documento, arquivos: dict):
        pass