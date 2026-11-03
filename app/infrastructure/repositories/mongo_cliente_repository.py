from uuid import UUID

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.domain.entities.cliente import Cliente
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.value_objects.documento import Documento


class MongoClienteRepository(ClienteRepository):

    def __init__(self, colecao: Collection):
        self.colecao = colecao
        self.colecao.create_index("documento", unique=True)

    @staticmethod
    def _para_documento(cliente: Cliente) -> dict:
        return {
            "id": str(cliente.id),
            "nome": cliente.nome,
            "email": cliente.email,
            "documento": cliente.documento.valor,
        }

    @staticmethod
    def _para_entidade(documento: dict) -> Cliente:
        return Cliente(
            id=UUID(documento["id"]),
            nome=documento["nome"],
            email=documento["email"],
            documento=Documento(documento["documento"]),
        )

    def salvar(self, cliente: Cliente) -> Cliente:
        dados = self._para_documento(cliente)

        try:
            self.colecao.replace_one(
                {"id": dados["id"]},
                dados,
                upsert=True,
            )
        except DuplicateKeyError as erro:
            raise ValueError(
                "Já existe um cliente com esse CPF ou CNPJ"
            ) from erro

        return cliente

    def buscar_por_id(self, cliente_id: UUID) -> Cliente | None:
        dados = self.colecao.find_one({"id": str(cliente_id)})

        if dados is None:
            return None

        return self._para_entidade(dados)

    def buscar_por_documento(self, documento: str) -> Cliente | None:
        documento_normalizado = Documento(documento).valor
        dados = self.colecao.find_one(
            {"documento": documento_normalizado}
        )

        if dados is None:
            return None

        return self._para_entidade(dados)

    def listar(self) -> list[Cliente]:
        documentos = self.colecao.find().sort("nome", 1)
        return [
            self._para_entidade(documento)
            for documento in documentos
        ]
