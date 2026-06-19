from app.models.dados_identificacao import DadosIdentificacao

class DadosIdentificacaoRepository:

    @staticmethod
    def buscar_por_candidatura(db, candidatura_id: int):

        return db.query(DadosIdentificacao).filter(DadosIdentificacao.candidatura_id==candidatura_id).first()

    @staticmethod
    def criar(db, dados):

        dados_identificacao = DadosIdentificacao(
            candidatura_id=dados.candidatura_id,
            nome_completo=dados.nome_completo,
            cpf=dados.cpf,
            rg=dados.rg,
            data_nascimento=dados.data_nascimento,
            nome_pai=dados.nome_pai,
            nome_mae=dados.nome_mae
        )

        db.add(dados_identificacao)

        db.flush()

        return dados_identificacao

    @staticmethod
    def atualizar(dados_identificacao, dados):

        dados_identificacao.nome_completo = dados.nome_completo
        dados_identificacao.cpf = dados.cpf
        dados_identificacao.rg = dados.rg
        dados_identificacao.data_nascimento = dados.data_nascimento
        dados_identificacao.nome_pai = dados.nome_pai
        dados_identificacao.nome_mae = dados.nome_mae

        return dados_identificacao