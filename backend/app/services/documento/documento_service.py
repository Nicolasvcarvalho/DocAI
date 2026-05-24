from fastapi import UploadFile
from pathlib import Path

from app.repositories.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.documento_repository import DocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.versao_documento_repository import VersaoDocumentoRepository
from app.repositories.arquivo_documento_repository import ArquivoDocumentoRepository

from app.services.file_storage_service import FileStorageService

from app.models.documento import Documento

from app.enums.status_documento import StatusDocumento
from app.enums.lado import Lado

from app.schemas.documento_schema import DocumentoCreateSchema, UploadDocumentoResponse
from app.schemas.versao_documento_schema import VersaoDocumentoCreateSchema
from app.schemas.arquivo_documento_schema import ArquivoDocumentoCreateSchema

class DocumentoService:

    @staticmethod
    def criar_documentos_iniciais(db, candidatura, candidato):
        
        tipos_documento = DocumentoService.obter_tipos_documento_obrigatorios(
            candidato,
            db
        )

        documentos = DocumentoService.montar_documentos(
            candidatura,
            tipos_documento
        )

        return documentos

    @staticmethod
    def obter_tipos_documento_obrigatorios(candidato, db):
        
        tipos_documentos = TipoDocumentoRepository.buscar_ativos(db)

        documentos_obrigatorios = []

        idade = candidato.calcular_idade()

        for tipo in tipos_documentos:

            obrigatorio = False

            if tipo.obrigatorio_base:
                obrigatorio = True

            if tipo.exige_maioridade and idade >= 18:
                obrigatorio = True

            if tipo.sexo_obrigatorio == candidato.sexo:
                obrigatorio = True

            if obrigatorio:            
                documentos_obrigatorios.append(tipo)

        return documentos_obrigatorios

    @staticmethod
    def montar_documentos(candidatura, tipos_documento):

        documentos = []

        for tipo in tipos_documento:

            documento = Documento(
                status = StatusDocumento.PENDENTE_ENVIO,
                candidatura_id = candidatura.id,
                tipo_documento_id = tipo.id
            )

            documentos.append(documento)
        
        return documentos
    
    @staticmethod
    def obter_contexto_documental(db, candidato):

        candidatura = CandidaturaRepository.buscar_por_candidato(db, candidato.id)
        documentos = DocumentoRepository.buscar_por_candidatura(db, candidatura.id)

        return documentos
    
    @staticmethod 
    def upload_documento(db, candidatura_id: int, tipo_documento_id: int, frente: UploadFile, verso: UploadFile):
        
        documento = DocumentoRepository.buscar_por_candidatura_e_tipo(
            db=db, candidatura_id=candidatura_id, tipo_documento_id=tipo_documento_id
        )

        if not documento:

            documento_dados = DocumentoCreateSchema(
                status=StatusDocumento.PENDENTE_ENVIO,
                candidatura_id=candidatura_id,
                tipo_documento_id=tipo_documento_id
            )
            documento = DocumentoRepository.criar(
                db=db,
                dados=documento_dados
            )
        
        ultima_versao = VersaoDocumentoRepository.buscar_ultima_versao(
            db=db,
            documento_id=documento.id
        )

        if not ultima_versao:
            nova_versao = 1

        else:
            nova_versao = ultima_versao + 1

        versao_documento_dados = VersaoDocumentoCreateSchema(
            documento_id=documento.id,
            versao=nova_versao
        )

        versao_documento = VersaoDocumentoRepository.criar(
            db, 
            dados=versao_documento_dados
        )

        pasta_versao = Path("storage")/"candidaturas"/f"candidatura_{candidatura_id}"/"documento_identificacao"/f"v{nova_versao}"

        path_frente = pasta_versao/"frente.png"
        caminho_frente = FileStorageService.salvar_arquivo(arquivo=frente, caminho=path_frente)

        path_verso = pasta_versao/"verso.png"
        caminho_verso = FileStorageService.salvar_arquivo(arquivo=verso, caminho=path_verso)

        arquivo_frente_dados = ArquivoDocumentoCreateSchema(
            versao_documento_id=versao_documento.id,
            lado=Lado.FRENTE,
            file_path=caminho_frente
        )
        ArquivoDocumentoRepository.criar(
            db=db,
            dados=arquivo_frente_dados
        )

        arquivo_verso_dados = ArquivoDocumentoCreateSchema(
            versao_documento_id=versao_documento.id,
            lado=Lado.VERSO,
            file_path=caminho_verso
        )
        ArquivoDocumentoRepository.criar(
            db=db,
            dados=arquivo_verso_dados
        )

        # Adicionar a referencia de versao_atual na tabela de documentos
        documento.versao_atual_id = versao_documento.id
        documento.status = StatusDocumento.ENVIADO

        db.commit()

        return UploadDocumentoResponse(
            documento_id=documento.id,
            versao_id=versao_documento.id,
            status=documento.status
        )




        
