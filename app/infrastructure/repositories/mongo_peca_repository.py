
from decimal import Decimal
from uuid import UUID

from pymongo.collection import Collection

from app.domain.entities.peca import Peca
from app.domain.repositories.peca_repository import PecaRepository


class MongoPecaRepository(PecaRepository):

    def __init__(self, colecao: Collection):
        self.colecao = colecao
        self.colecao.create_index("nome")

    @staticmethod
    def _para_documento(peca: Peca) -> dict:
        return {
            "id": str(peca.id),
            "nome": peca.nome,
            "preco": str(peca.preco),
            "quantidade_estoque": peca.quantidade_estoque,
            "ativa": peca.ativa,
        }

    @staticmethod
    def _para_entidade(documento: dict) -> Peca:
        return Peca(
            id=UUID(documento["id"]),
            nome=documento["nome"],
            preco=Decimal(documento["preco"]),
            quantidade_estoque=documento["quantidade_estoque"],
            ativa=documento["ativa"],
        )

    def salvar(self, peca: Peca) -> Peca:
        dados = self._para_documento(peca)
        self.colecao.replace_one(
            {"id": dados["id"]},
            dados,
            upsert=True,
        )
        return peca

    def buscar_por_id(self, peca_id: UUID) -> Peca | None:
        dados = self.colecao.find_one({"id": str(peca_id)})

        if dados is None:
            return None

        return self._para_entidade(dados)

    def listar(self) -> list[Peca]:
        documentos = self.colecao.find().sort("nome", 1)
        return [
            self._para_entidade(documento)
            for documento in documentos
        ]
