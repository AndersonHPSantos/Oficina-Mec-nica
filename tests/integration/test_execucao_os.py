from uuid import uuid4
from contextlib import contextmanager
from decimal import Decimal

import pytest

from app.application.use_cases.ordens_servico.iniciar_execucao import (
    IniciarExecucao,
)
from app.domain.entities.ordem_servico import OrdemServico
from app.domain.entities.item_os import ItemOS
from app.domain.enums.status_os import StatusOS, StatusOrcamento


class RepositorioOrdensFake:
    def __init__(self, ordem):
        self.ordem = ordem
        self.salva = False

    def buscar_por_id(self, ordem_id, session=None):
        return self.ordem if self.ordem.id == ordem_id else None

    def salvar(self, ordem, session=None):
        self.ordem = ordem
        self.salva = True


class RepositorioPecasFake:
    def __init__(self, estoques):
        self.estoques = estoques

    def baixar_estoque(self, peca_id, quantidade, session=None):
        estoque = self.estoques.get(peca_id, 0)

        if estoque < quantidade:
            return False

        self.estoques[peca_id] -= quantidade
        return True


class UnidadeTrabalhoFake:
    @contextmanager
    def transacao(self):
        yield object()


def criar_ordem_com_pecas(estoque_inicial):
    ordem = OrdemServico(
        cliente_id=uuid4(),
        veiculo_id=uuid4(),
    )

    peca_id = uuid4()

    ordem.status = StatusOS.AGUARDANDO_APROVACAO
    ordem.status_orcamento = StatusOrcamento.APROVADO
    ordem.itens = [
        ItemOS(
            descricao="Filtro de óleo",
            quantidade=2,
            preco_unitario=Decimal("30.00"),
            tipo="peca",
            referencia_id=peca_id,
        )
    ]

    ordens = RepositorioOrdensFake(ordem)
    pecas = RepositorioPecasFake({peca_id: estoque_inicial})

    caso_de_uso = IniciarExecucao(
        ordens,
        pecas,
        UnidadeTrabalhoFake(),
    )

    return caso_de_uso, ordem, ordens, pecas, peca_id


def test_execucao_desconta_estoque():
    caso, ordem, ordens, pecas, peca_id = criar_ordem_com_pecas(5)

    resultado = caso.executar(str(ordem.id))

    assert resultado.status == StatusOS.EM_EXECUCAO
    assert pecas.estoques[peca_id] == 3
    assert ordens.salva is True


def test_execucao_rejeita_estoque_insuficiente():
    caso, ordem, ordens, pecas, peca_id = criar_ordem_com_pecas(1)

    with pytest.raises(ValueError, match="Estoque insuficiente"):
        caso.executar(str(ordem.id))

    assert pecas.estoques[peca_id] == 1
    assert ordens.salva is False


def test_execucao_rejeita_os_inexistente():
    caso, _, _, _, _ = criar_ordem_com_pecas(5)

    with pytest.raises(ValueError, match="não encontrada"):
        caso.executar(str(uuid4()))