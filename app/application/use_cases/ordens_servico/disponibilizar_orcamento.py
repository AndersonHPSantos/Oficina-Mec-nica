
from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class DisponibilizarOrcamento:

    def __init__(self, ordens: OrdemServicoRepository):
        self.ordens = ordens

    def executar(self, ordem_id: str):
        from uuid import UUID

        try:
            identificador = UUID(ordem_id)
        except (ValueError, TypeError, AttributeError) as erro:
            raise ValueError("Identificador da OS inválido") from erro

        ordem = self.ordens.buscar_por_id(identificador)

        if ordem is None:
            raise ValueError("Ordem de serviço não encontrada")

        ordem.disponibilizar_orcamento()
        self.ordens.salvar(ordem)

        return ordem
