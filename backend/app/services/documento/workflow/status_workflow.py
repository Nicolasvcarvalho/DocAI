from fastapi import HTTPException

from app.models.documento import Documento

from app.enums.status_documento import StatusDocumento

class StatusWorkflow:
    
    TRANSICOES_VALIDAS = {

        StatusDocumento.PENDENTE_ENVIO: (
            StatusDocumento.ENVIADO
        ),

        StatusDocumento.ENVIADO: (
            StatusDocumento.PROCESSANDO
        ),

        StatusDocumento.PROCESSANDO: (
            StatusDocumento.AGUARDANDO_CONFIRMACAO
        ),

        StatusDocumento.AGUARDANDO_CONFIRMACAO: (
            StatusDocumento.PROCESSADO
        ),

        StatusDocumento.PROCESSADO: (
            StatusDocumento.EM_ANALISE
        ),

        StatusDocumento.EM_ANALISE: (
            StatusDocumento.APROVADO,
            StatusDocumento.REJEITADO
        ),

        StatusDocumento.REJEITADO: (
            StatusDocumento.ENVIADO
        ), 

        StatusDocumento.APROVADO: tuple()
    }

    STATUS_PERMITEM_REENVIO = {

        StatusDocumento.PENDENTE_ENVIO,
        StatusDocumento.REJEITADO
    }

    @staticmethod
    def _validar_transicao(status_atual: StatusDocumento, novo_status: StatusDocumento):
        
        transicoes_permitidas = StatusWorkflow.TRANSICOES_VALIDAS.get(status_atual, tuple())

        if novo_status not in transicoes_permitidas:
            raise HTTPException(status_code=400, detail=f"Transição de status inválida: {status_atual} -> {novo_status}")
        
    @staticmethod
    def transicionar_status(documento: Documento, novo_status: StatusDocumento):

        StatusWorkflow._validar_transicao(documento.status, novo_status)

        documento.status = novo_status

    @staticmethod
    def validar_reenvio(documento: Documento):

        if documento.status not in StatusWorkflow.STATUS_PERMITEM_REENVIO:
            raise HTTPException(status_code=400, detail=f"Documento não permite reenvio no status atual: {documento.status}")
        