
from app.domain.entities.cliente import Cliente
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.value_objects.documento import Documento


class CadastrarCliente:

    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def executar(
        self,
        nome: str,
        email: str,
        documento: str,
    ) -> Cliente:
        documento_validado = Documento(documento)

        cliente_existente = self.repositorio.buscar_por_documento(
            documento_validado.valor
        )

        if cliente_existente is not None:
            raise ValueError("Já existe um cliente com esse CPF ou CNPJ")

        cliente = Cliente(
            nome=nome,
            email=email,
            documento=documento_validado,
        )

        return self.repositorio.salvar(cliente)
