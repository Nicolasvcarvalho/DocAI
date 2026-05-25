from app.repositories.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.documento_repository import DocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.versao_documento_repository import VersaoDocumentoRepository

from app.services.documento.processors.processor_factory import DocumentoProcessorFactory

from app.models.documento import Documento

from app.enums.status_documento import StatusDocumento

from app.schemas.documento_schema import DocumentoCreateSchema
from app.schemas.versao_documento_schema import VersaoDocumentoCreateSchema
from app.schemas.upload_documento_schema import DocumentoUploadInput

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
    def upload_documento(db, candidatura_id: int, tipo_documento, arquivos: DocumentoUploadInput):
        
        documento = DocumentoRepository.buscar_por_candidatura_e_tipo(
            db=db, candidatura_id=candidatura_id, tipo_documento_id=tipo_documento.id
        )

        if not documento:

            documento_dados = DocumentoCreateSchema(
                status=StatusDocumento.PENDENTE_ENVIO,
                candidatura_id=candidatura_id,
                tipo_documento_id=tipo_documento.id
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

        processor = DocumentoProcessorFactory.get_processor(tipo_documento.nome)
        processor.processar_upload(db=db, documento=documento, versao_documento=versao_documento, arquivos=arquivos)

        documento.versao_atual_id = versao_documento.id
        documento.status = StatusDocumento.ENVIADO

        db.commit()

        return documento