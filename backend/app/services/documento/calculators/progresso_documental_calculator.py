from app.enums.status_documento import StatusDocumento
from app.models.candidatura import Candidatura

class ProgressoDocumentalCalculator:

    @staticmethod
    def calcular(candidatura: Candidatura) -> dict:

        documentos = candidatura.documentos

        total = len(documentos)

        enviados = len([
            documento for documento in documentos 
            if documento.status != StatusDocumento.PENDENTE_ENVIO
        ])

        aprovados = len([
            documento for documento in documentos
            if documento.status==StatusDocumento.APROVADO
        ])

        rejeitados = len([
            documento for documento in documentos
            if documento.status==StatusDocumento.REJEITADO
        ])

        percentual = 0

        if total > 0:
            percentual = int((aprovados / total) * 100)

        return {
            "total": total,
            "enviados": enviados,
            "aprovados": aprovados,
            "rejeitados": rejeitados,
            "percentual": percentual
        }