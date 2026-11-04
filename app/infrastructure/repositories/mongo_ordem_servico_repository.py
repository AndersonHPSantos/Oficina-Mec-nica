
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from pymongo.collection import Collection

from app.domain.entities.item_os import ItemOS
from app.domain.entities.ordem_servico import OrdemServico
from app.domain.enums.status_os import StatusOS, StatusOrcamento
from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class MongoOrdemServicoRepository(OrdemServicoRepository):

    def __init__(self, colecao: Collection):
        self.colecao = colecao
        self.colecao.create_index("cliente_id")
        self.colecao.create_index("status")

    @staticmethod
    def _data_para_texto(data: datetime | None) -> str | None:
        return data.isoformat() if data is not None else None

    @staticmethod
    def _texto_para_data(valor: str | None) -> datetime | None:
        if valor is None:
            return None

        data = datetime.fromisoformat(valor)

        if data.tzinfo is None:
            data = data.replace(tzinfo=timezone.utc)

        return data

    @classmethod
    def _para_documento(cls, ordem: OrdemServico) -> dict:
        return {
            "id": str(ordem.id),
            "cliente_id": str(ordem.cliente_id),
            "veiculo_id": str(ordem.veiculo_id),
            "status": ordem.status.value,
            "status_orcamento": ordem.status_orcamento.value,
            "valor_orcamento": str(ordem.valor_orcamento),
            "criada_em": cls._data_para_texto(ordem.criada_em),
            "diagnostico_em": cls._data_para_texto(ordem.diagnostico_em),
            "iniciada_em": cls._data_para_texto(ordem.iniciada_em),
            "finalizada_em": cls._data_para_texto(ordem.finalizada_em),
            "entregue_em": cls._data_para_texto(ordem.entregue_em),
            "itens": [
                {
                    "descricao": item.descricao,
                    "quantidade": item.quantidade,
                    "preco_unitario": str(item.preco_unitario),
                    "tipo": item.tipo,
                    "referencia_id": str(item.referencia_id),
                }
                for item in ordem.itens
            ],
        }

    @classmethod
    def _para_entidade(cls, documento: dict) -> OrdemServico:
        ordem = OrdemServico(
            id=UUID(documento["id"]),
            cliente_id=UUID(documento["cliente_id"]),
            veiculo_id=UUID(documento["veiculo_id"]),
            status=StatusOS(documento["status"]),
            status_orcamento=StatusOrcamento(
                documento["status_orcamento"]
            ),
            valor_orcamento=Decimal(documento["valor_orcamento"]),
            criada_em=cls._texto_para_data(documento["criada_em"]),
            diagnostico_em=cls._texto_para_data(
                documento.get("diagnostico_em")
            ),
            iniciada_em=cls._texto_para_data(
                documento.get("iniciada_em")
            ),
            finalizada_em=cls._texto_para_data(
                documento.get("finalizada_em")
            ),
            entregue_em=cls._texto_para_data(
                documento.get("entregue_em")
            ),
        )

        ordem.itens = [
            ItemOS(
                descricao=item["descricao"],
                quantidade=item["quantidade"],
                preco_unitario=Decimal(item["preco_unitario"]),
                tipo=item["tipo"],
                referencia_id=UUID(item["referencia_id"]),
            )
            for item in documento.get("itens", [])
        ]

        return ordem

    def salvar(self, ordem, session=None):
        documento = self._para_documento(ordem)

        self.collection.replace_one(
            {"id": str(ordem.id)},
            documento,
            upsert=True,
            session=session,
        )

    def buscar_por_id(self, ordem_id, session=None):
        documento = self.collection.find_one(
            {"id": str(ordem_id)},
            session=session,
        )

        if documento is None:
            return None

        return self._para_entidade(documento)

    def listar_por_cliente(
        self,
        cliente_id: UUID,
    ) -> list[OrdemServico]:
        documentos = self.colecao.find(
            {"cliente_id": str(cliente_id)}
        ).sort("criada_em", -1)

        return [
            self._para_entidade(documento)
            for documento in documentos
        ]
