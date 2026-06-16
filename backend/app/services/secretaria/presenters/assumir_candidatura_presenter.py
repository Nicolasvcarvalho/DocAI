from app.schemas.secretaria.assumir_candidatura_schema import AssumirCandidaturaResponse

class AssumirCandidaturaPresenter:

    @staticmethod
    def montar(candidatura):

        return AssumirCandidaturaResponse(
                id=candidatura.id,
                status=candidatura.status,
                locked_by_id=candidatura.locked_by_id,
                mensagem="Candidatura assumida com sucesso"
            )
            