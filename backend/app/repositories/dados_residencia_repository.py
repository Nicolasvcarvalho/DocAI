from app.models.dados_residencia import DadosResidencia

class DadosResidenciaRepository:

    @staticmethod
    def buscar_por_candidatura(db, candidatura_id: int):

        return db.query(DadosResidencia).filter(DadosResidencia.candidatura_id==candidatura_id).first()

    @staticmethod
    def criar(db, dados):

        dados_residencia = DadosResidencia(
            candidatura_id=dados.candidatura_id,
            logradouro=dados.logradouro,
            numero=dados.numero,
            bairro=dados.bairro,
            cidade=dados.cidade,
            estado=dados.estado,
            cep=dados.cep
        )

        db.add(dados_residencia)

        db.flush()

        return dados_residencia

    @staticmethod
    def atualizar(dados_residencia, dados):

        dados_residencia.logradouro = dados.logradouro
        dados_residencia.numero = dados.numero
        dados_residencia.bairro = dados.bairro
        dados_residencia.cidade = dados.cidade
        dados_residencia.estado = dados.estado
        dados_residencia.cep = dados.cep

        return dados_residencia