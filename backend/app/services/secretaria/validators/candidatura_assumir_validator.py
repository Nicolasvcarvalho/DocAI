from fastapi import HTTPException

from app.enums.status_candidatura import StatusCandidatura


class CandidaturaAssumirValidator:

    @staticmethod
    def validar(candidatura):

        if candidatura.status != StatusCandidatura.DOCUMENTACAO_PENDENTE:
            raise HTTPException(status_code=400, detail="A candidatura não está disponível para análise")

        if candidatura.possui_analista:
            raise HTTPException(status_code=409, detail=("Candidatura em análise por outra secretaria"))