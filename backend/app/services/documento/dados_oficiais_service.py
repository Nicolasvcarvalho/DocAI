from app.repositories.dados_identificacao_repository import DadosIdentificacaoRepository
from app.repositories.dados_residencia_repository import DadosResidenciaRepository

from app.schemas.dados_identificacao_schema import DadosIdentificacaoCreateSchema
from app.schemas.dados_residencia_schema import DadosResidenciaCreateSchema


class DadosOficiaisService:

    @staticmethod
    def persistir(db, documento):

        PERSISTORS = {
            "DOCUMENTO_IDENTIFICACAO": DadosOficiaisService._persistir_identificacao,
            "COMPROVANTE_RESIDENCIA": DadosOficiaisService._persistir_residencia,
        }

        nome_documento = documento.tipo_documento.nome

        persistor = PERSISTORS.get(nome_documento)
        persistor(db, documento) 

    @staticmethod
    def _persistir_identificacao(db, documento):

        candidatura = documento.candidatura

        ocr = documento.versao_atual.ocr_resultado

        dados = ocr.dados_json

        schema = DadosIdentificacaoCreateSchema(
            candidatura_id=candidatura.id,
            nome_completo=dados.get("nome"),
            cpf=dados.get("cpf"),
            rg=dados.get("rg"),
            data_nascimento=dados.get("data_nascimento"),
            nome_pai=dados.get("nome_pai"),
            nome_mae=dados.get("nome_mae")
        )

        existente = DadosIdentificacaoRepository.buscar_por_candidatura(db, candidatura.id)

        if existente:
            DadosIdentificacaoRepository.atualizar(existente, schema)

        else:
            DadosIdentificacaoRepository.criar(db, schema)

    @staticmethod
    def _persistir_residencia(db, documento):

        candidatura = documento.candidatura

        ocr = documento.versao_atual.ocr_resultado

        dados = ocr.dados_json

        schema = DadosResidenciaCreateSchema(
            candidatura_id=candidatura.id,
            logradouro=dados.get("logradouro"),
            numero=dados.get("numero"),
            bairro=dados.get("bairro"),
            cidade=dados.get("cidade"),
            estado=dados.get("estado"),
            cep=dados.get("cep")
        )

        existente = DadosResidenciaRepository.buscar_por_candidatura(db, candidatura.id)

        if existente:
            DadosResidenciaRepository.atualizar(existente, schema)

        else:
            DadosResidenciaRepository.criar(db, schema)