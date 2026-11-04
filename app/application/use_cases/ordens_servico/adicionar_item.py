
from uuid import UUID

from app.domain.entities.item_os import ItemOS
from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)
from app.domain.repositories.servico_repository import ServicoRepository
from app.domain.repositories.peca_repository import PecaRepository


class AdicionarItemOS:

    def __init__(
        self,
        ordens: OrdemServicoRepository,
        servicos: ServicoRepository,
        pecas: PecaRepository,
    ):
        self.ordens = ordens
        self.servicos = servicos
        self.pecas = pecas

    def executar(
        self,
        ordem_id: str,
        tipo: str,
        referencia_id: str,
        quantidade: int = 1,
    ):
        try:
            id_ordem = UUID(ordem_id)
            id_referencia = UUID(referencia_id)
        except (ValueError, TypeError, AttributeError) as erro:
            raise ValueError("Identificador inválido") from erro

        ordem = self.ordens.buscar_por_id(id_ordem)

        if ordem is None:
            raise ValueError("Ordem de serviço não encontrada")

        if tipo == "servico":
            catalogo = self.servicos
            item_catalogo = catalogo.buscar_por_id(id_referencia)

            if item_catalogo is None or not item_catalogo.ativo:
                raise ValueError("Serviço não encontrado ou inativo")

            descricao = item_catalogo.nome
            preco = item_catalogo.preco

        elif tipo == "peca":
            catalogo = self.pecas
            item_catalogo = catalogo.buscar_por_id(id_referencia)

            if item_catalogo is None or not item_catalogo.ativa:
                raise ValueError("Peça não encontrada ou inativa")

            if quantidade > item_catalogo.quantidade_estoque:
                raise ValueError("Estoque insuficiente")

            descricao = item_catalogo.nome
            preco = item_catalogo.preco

        else:
            raise ValueError("Tipo deve ser 'servico' ou 'peca'")

        item = ItemOS(
            descricao=descricao,
            quantidade=quantidade,
            preco_unitario=preco,
            tipo=tipo,
            referencia_id=id_referencia,
        )

        ordem.adicionar_item(item)
        self.ordens.salvar(ordem)

        return ordem
