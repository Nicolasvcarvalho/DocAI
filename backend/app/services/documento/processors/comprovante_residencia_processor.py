from pathlib import Path

from app.services.documento.processors.base_processor import DocumentoProcessor

from app.services.file_storage_service import FileStorageService

from app.schemas.arquivo_documento_schema import ArquivoDocumentoCreateSchema

from app.repositories.arquivo_documento_repository import ArquivoDocumentoRepository

from app.enums.lado import Lado

class ComprovanteResidenciaProcessor(DocumentoProcessor):

    def processar_upload(self, db, documento, versao_documento, arquivos):
        
        pasta = Path("storage")/"candidaturas"/f"candidatura_{documento.candidatura_id}"/"comprovante_residencia"/f"v{versao_documento.versao}"

        extensao_arquivo = Path(arquivos.arquivo.filename).suffix.lower()
        caminho_arquivo = pasta/f"comprovante{extensao_arquivo}"

        path_arquivo = FileStorageService.salvar_arquivo(arquivo=arquivos.arquivo, caminho=caminho_arquivo)

        ArquivoDocumentoRepository.criar(db=db, dados=ArquivoDocumentoCreateSchema(
            versao_documento_id=versao_documento.id,
            lado=Lado.UNICO,
            file_path=str(path_arquivo)
        ))