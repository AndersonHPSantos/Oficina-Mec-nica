
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.ordem_servico import OrdemServico


class OrdemServicoRepository(ABC):

    @abstractmethod
    def salvar(self, ordem: OrdemServico) -> OrdemServico:
        pass

    @abstractmethod
    def buscar_por_id(
        self,
        ordem_id: UUID,
    ) -> OrdemServico | None:
        pass

    @abstractmethod
    def listar_por_cliente(
        self,
        cliente_id: UUID,
    ) -> list[OrdemServico]:
        pass
