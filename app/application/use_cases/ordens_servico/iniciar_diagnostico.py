
from uuid import UUID

from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class IniciarDiagnostico:

    def __init__(self, ordens: OrdemServicoRepository):
        self.ordens = ordens

    def executar(self, ordem_id: str):
        try:
            identificador = UUID(ordem_id)
        except (ValueError, TypeError, AttributeError) as erro:
            raise ValueError("Identificador da OS inválido") from erro

        ordem = self.ordens.buscar_por_id(identificador)

        if ordem is None:
            raise ValueError("Ordem de serviço não encontrada")

        ordem.iniciar_diagnostico()
        self.ordens.salvar(ordem)

        return ordem
