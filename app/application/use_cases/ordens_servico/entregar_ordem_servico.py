from uuid import UUID
from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class EntregarOrdemServico:
    def __init__(self, ordens: OrdemServicoRepository):
        self.ordens = ordens

    def executar(self, ordem_id: str):
        try:
            id_uuid = UUID(ordem_id)
        except ValueError:
            raise ValueError("ID da Ordem de Serviço inválido.")

        ordem = self.ordens.buscar_por_id(id_uuid)

        if ordem is None:
            raise ValueError("Ordem de Serviço não encontrada.")

        ordem.entregar()
        self.ordens.salvar(ordem)

        return ordem