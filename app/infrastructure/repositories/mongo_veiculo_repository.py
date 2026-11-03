
from uuid import UUID

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.domain.entities.veiculo import Veiculo
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.domain.value_objects.placa import Placa


class MongoVeiculoRepository(VeiculoRepository):

    def __init__(self, colecao: Collection):
        self.colecao = colecao
        self.colecao.create_index("placa", unique=True)
        self.colecao.create_index("cliente_id")

    @staticmethod
    def _para_documento(veiculo: Veiculo) -> dict:
        return {
            "id": str(veiculo.id),
            "cliente_id": str(veiculo.cliente_id),
            "placa": veiculo.placa.valor,
            "marca": veiculo.marca,
            "modelo": veiculo.modelo,
            "ano": veiculo.ano,
        }

    @staticmethod
    def _para_entidade(documento: dict) -> Veiculo:
        return Veiculo(
            id=UUID(documento["id"]),
            cliente_id=UUID(documento["cliente_id"]),
            placa=Placa(documento["placa"]),
            marca=documento["marca"],
            modelo=documento["modelo"],
            ano=documento["ano"],
        )

    def salvar(self, veiculo: Veiculo) -> Veiculo:
        dados = self._para_documento(veiculo)

        try:
            self.colecao.replace_one(
                {"id": dados["id"]},
                dados,
                upsert=True,
            )
        except DuplicateKeyError as erro:
            raise ValueError(
                "Já existe um veículo cadastrado com essa placa"
            ) from erro

        return veiculo

    def buscar_por_id(self, veiculo_id: UUID) -> Veiculo | None:
        dados = self.colecao.find_one({"id": str(veiculo_id)})

        if dados is None:
            return None

        return self._para_entidade(dados)

    def buscar_por_placa(self, placa: str) -> Veiculo | None:
        placa_normalizada = Placa(placa).valor
        dados = self.colecao.find_one({"placa": placa_normalizada})

        if dados is None:
            return None

        return self._para_entidade(dados)

    def listar_por_cliente(self, cliente_id: UUID) -> list[Veiculo]:
        documentos = self.colecao.find(
            {"cliente_id": str(cliente_id)}
        ).sort("placa", 1)

        return [
            self._para_entidade(documento)
            for documento in documentos
        ]
