from app.repositories.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.documento_repository import DocumentoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.models.documento import Documento
from app.enums.status_documento import StatusDocumento

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