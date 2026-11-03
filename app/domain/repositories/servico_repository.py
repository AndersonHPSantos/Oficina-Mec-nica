
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.servico import Servico


class ServicoRepository(ABC):

    @abstractmethod
    def salvar(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    def buscar_por_id(self, servico_id: UUID) -> Servico | None:
        pass

    @abstractmethod
    def listar(self) -> list[Servico]:
        pass
