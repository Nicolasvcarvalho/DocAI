from app.repositories.tipo_documento_repository import TipoDocumentoRepository

class DocumentoService:

    @staticmethod
    def calcular_documentos_obrigatorios(candidato, db):
        
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



        