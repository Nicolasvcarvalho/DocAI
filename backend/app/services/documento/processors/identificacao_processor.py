from pathlib import Path

from sqlalchemy.orm import Session

from app.schemas.upload_documento_schema import DocumentoUploadInput
from app.schemas.arquivo_documento_schema import ArquivoDocumentoCreateSchema

from app.repositories.arquivo_documento_repository import ArquivoDocumentoRepository

from app.services.file_storage_service import FileStorageService
from app.services.documento.processors.base_processor import DocumentoProcessor

from app.enums.lado import Lado

class DocumentoIdentificaoProcessor(DocumentoProcessor):

    def processar_upload(self, db, documento, versao_documento, arquivos):
        
        pasta = Path("storage")/"candidaturas"/f"candidatura_{documento.candidatura_id}"/"documento_identificacao"/f"v{versao_documento.versao}"

        caminho_frente = pasta/"frente.png"
        caminho_verso = pasta/"verso.png"

        path_frente = FileStorageService.salvar_arquivo(arquivo=arquivos.frente, caminho=caminho_frente)
        path_verso = FileStorageService.salvar_arquivo(arquivo=arquivos.verso, caminho=caminho_verso)

        ArquivoDocumentoRepository.criar(
            db=db,
            dados=ArquivoDocumentoCreateSchema(
                versao_documento_id=versao_documento.id,
                lado=Lado.FRENTE,
                file_path=path_frente
            )
        )

        ArquivoDocumentoRepository.criar(
            db=db,
            dados=ArquivoDocumentoCreateSchema(
                versao_documento_id=versao_documento.id,
                lado=Lado.VERSO,
                file_path=path_verso
            )
        )