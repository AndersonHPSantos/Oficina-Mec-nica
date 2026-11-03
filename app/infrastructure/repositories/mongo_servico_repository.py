
from decimal import Decimal
from uuid import UUID

from pymongo.collection import Collection

from app.domain.entities.servico import Servico
from app.domain.repositories.servico_repository import ServicoRepository


class MongoServicoRepository(ServicoRepository):

    def __init__(self, colecao: Collection):
        self.colecao = colecao
        self.colecao.create_index("nome")

    @staticmethod
    def _para_documento(servico: Servico) -> dict:
        return {
            "id": str(servico.id),
            "nome": servico.nome,
            "descricao": servico.descricao,
            "preco": str(servico.preco),
            "tempo_estimado_minutos": servico.tempo_estimado_minutos,
            "ativo": servico.ativo,
        }

    @staticmethod
    def _para_entidade(documento: dict) -> Servico:
        return Servico(
            id=UUID(documento["id"]),
            nome=documento["nome"],
            descricao=documento["descricao"],
            preco=Decimal(documento["preco"]),
            tempo_estimado_minutos=documento["tempo_estimado_minutos"],
            ativo=documento["ativo"],
        )

    def salvar(self, servico: Servico) -> Servico:
        dados = self._para_documento(servico)
        self.colecao.replace_one(
            {"id": dados["id"]},
            dados,
            upsert=True,
        )
        return servico

    def buscar_por_id(self, servico_id: UUID) -> Servico | None:
        dados = self.colecao.find_one({"id": str(servico_id)})

        if dados is None:
            return None

        return self._para_entidade(dados)

    def listar(self) -> list[Servico]:
        documentos = self.colecao.find().sort("nome", 1)
        return [
            self._para_entidade(documento)
            for documento in documentos
        ]
