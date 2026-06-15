from app.enums.status_documento import StatusDocumento
from app.models.documento import Documento

class DocumentoPermissionService:

    @staticmethod
    def obter_acoes_permitidas(documento: Documento) -> dict:
        
        status = documento.status

        return {
            "pode_visualizar_arquivo": status != StatusDocumento.PENDENTE_ENVIO,
            "pode_enviar_documento": status == StatusDocumento.PENDENTE_ENVIO,
            "pode_reenviar_documento": status == StatusDocumento.AGUARDANDO_REENVIO,
            "pode_confirmar_ocr": status == StatusDocumento.AGUARDANDO_CONFIRMACAO,
            "pode_editar_dados_ocr": status == StatusDocumento.AGUARDANDO_CONFIRMACAO 
        }