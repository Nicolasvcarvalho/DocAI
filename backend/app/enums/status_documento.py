from enum import Enum

class StatusDocumento(str, Enum):

    PENDENTE_ENVIO = "PENDENTE_ENVIO"
    ENVIADO = "ENVIADO"
    PROCESSANDO = "PROCESSANDO"
    AGUARDANDO_CONFIRMACAO = "AGUARDANDO_CONFIRMACAO"
    PROCESSADO = "PROCESSADO"
    EM_ANALISE = "EM_ANALISE"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO" 

    # Add o processado para se referir o momento em que foi  processado mas nao aanalisado   