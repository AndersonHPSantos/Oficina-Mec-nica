
from app.domain.entities.cliente import Cliente
from app.domain.repositories.cliente_repository import ClienteRepository


class ListarClientes:

    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def executar(self) -> list[Cliente]:
        return self.repositorio.listar()
