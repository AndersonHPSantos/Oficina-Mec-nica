from enum import Enum

class StatusOS(str, Enum):
    RECEBIDA = "Recebida"
    EM_DIAGNOSTICO = "Em diagnóstico"
    AGUARDANDO_APROVACAO = "Aguardando aprovação"
    EM_EXECUCAO = "Em execução"
    FINALIZADA = "Finalizada"
    ENTREGUE = "Entregue"


class StatusOrcamento(str, Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"