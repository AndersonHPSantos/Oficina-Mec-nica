from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.cliente import Cliente


class ClienteRepository(ABC):

    @abstractmethod
    def salvar(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def buscar_por_id(self, cliente_id: UUID) -> Cliente | None:
        pass

    @abstractmethod
    def buscar_por_documento(self, documento: str) -> Cliente | None:
        pass

    @abstractmethod
    def listar(self) -> list[Cliente]:
        pass
