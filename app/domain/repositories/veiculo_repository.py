
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.veiculo import Veiculo


class VeiculoRepository(ABC):

    @abstractmethod
    def salvar(self, veiculo: Veiculo) -> Veiculo:
        pass

    @abstractmethod
    def buscar_por_id(self, veiculo_id: UUID) -> Veiculo | None:
        pass

    @abstractmethod
    def buscar_por_placa(self, placa: str) -> Veiculo | None:
        pass

    @abstractmethod
    def listar_por_cliente(self, cliente_id: UUID) -> list[Veiculo]:
        pass
