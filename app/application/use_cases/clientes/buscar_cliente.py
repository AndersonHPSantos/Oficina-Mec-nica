
from uuid import UUID

from app.domain.entities.cliente import Cliente
from app.domain.repositories.cliente_repository import ClienteRepository


class BuscarCliente:

    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def executar(self, cliente_id: str) -> Cliente | None:
        try:
            identificador = UUID(cliente_id)
        except (ValueError, TypeError, AttributeError):
            raise ValueError("Identificador do cliente inválido")

        return self.repositorio.buscar_por_id(identificador)
