
from uuid import UUID

from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class DecidirOrcamento:

    def __init__(self, ordens: OrdemServicoRepository):
        self.ordens = ordens

    def executar(self, ordem_id: str, aprovado: bool):
        try:
            identificador = UUID(ordem_id)
        except (ValueError, TypeError, AttributeError) as erro:
            raise ValueError("Identificador da OS inválido") from erro

        ordem = self.ordens.buscar_por_id(identificador)

        if ordem is None:
            raise ValueError("Ordem de serviço não encontrada")

        if aprovado:
            ordem.aprovar_orcamento()
        else:
            ordem.rejeitar_orcamento()

        self.ordens.salvar(ordem)

        return ordem
