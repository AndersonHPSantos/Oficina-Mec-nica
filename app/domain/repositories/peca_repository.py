
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.peca import Peca


class PecaRepository(ABC):

    @abstractmethod
    def salvar(self, peca: Peca) -> Peca:
        pass

    @abstractmethod
    def buscar_por_id(self, peca_id: UUID) -> Peca | None:
        pass

    @abstractmethod
    def listar(self) -> list[Peca]:
        pass
