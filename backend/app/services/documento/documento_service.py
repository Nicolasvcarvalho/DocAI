from app.repositories.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.documento_repository import DocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.versao_documento_repository import VersaoDocumentoRepository

from app.services.documento.processors.processor_factory import DocumentoProcessorFactory

from app.services.documento.workflow.documento_status_workflow import DocumentoStatusWorkflow

from app.services.documento.validators.upload_validator import UploadValidator
from app.services.documento.validators.ownership_validator import OwnershipValidator
from app.services.documento.validators.lado_documento_validator import LadoDocumentoValidator

from app.models.documento import Documento
from app.models.usuario import Usuario
from app.models.candidatura import Candidatura
from app.models.tipo_documento import TipoDocumento
from app.models.versao_documento import VersaoDocumento

from app.enums.status_documento import StatusDocumento

from app.schemas.documento_schema import DocumentoCreateSchema
from app.schemas.versao_documento_schema import VersaoDocumentoCreateSchema
from app.schemas.upload_documento_schema import DocumentoUploadInput

from sqlalchemy.orm import Session

class DocumentoService:

    @staticmethod
    def criar_documentos_iniciais(db, candidatura, candidato):
        
        tipos_documento = DocumentoService._obter_tipos_documento_obrigatorios(
            candidato,
            db
        )

        documentos = DocumentoService._montar_documentos(
            candidatura,
            tipos_documento
        )

        return documentos

    @staticmethod
    def _obter_tipos_documento_obrigatorios(candidato, db):
        
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
    def _montar_documentos(candidatura, tipos_documento):

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
    async def upload_documento(db, candidato: Usuario, candidatura: Candidatura, tipo_documento: TipoDocumento, arquivos: DocumentoUploadInput) -> Documento:

        LadoDocumentoValidator.validar_lados_documento(tipo_documento, arquivos)
        OwnershipValidator.validar_candidatura_usuario(candidato, candidatura)

        await UploadValidator.validar_upload(arquivos)

        documento = DocumentoRepository.buscar_por_candidatura_e_tipo(
            db=db, candidatura_id=candidatura.id, tipo_documento_id=tipo_documento.id
        )

        if not documento:

            documento_dados = DocumentoCreateSchema(
                status=StatusDocumento.PENDENTE_ENVIO,
                candidatura_id=candidatura.id,
                tipo_documento_id=tipo_documento.id
            )
            documento = DocumentoRepository.criar(
                db=db,
                dados=documento_dados
            )
        
        else:
            OwnershipValidator.validar_documento_candidatura(documento, candidatura)
            DocumentoStatusWorkflow.validar_reenvio(documento)
        
        versao_documento = DocumentoService._criar_nova_versao(db, documento)   
             
        processor = DocumentoProcessorFactory.get_processor(tipo_documento.nome)
        processor.processar_upload(db=db, documento=documento, versao_documento=versao_documento, arquivos=arquivos)

        documento.versao_atual_id = versao_documento.id
        DocumentoStatusWorkflow.transicionar_status_documento(db, documento, StatusDocumento.ENVIADO)

        db.commit()

        return documento

    @staticmethod
    def _criar_nova_versao(db: Session, documento: Documento) -> VersaoDocumento:
        
        ultima_versao = VersaoDocumentoRepository.buscar_ultima_versao(db, documento.id)

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

        return versao_documento
    