
from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.entities.servico import Servico
from app.domain.entities.peca import Peca


def test_criar_servico():
    servico = Servico(
        nome="Troca de óleo",
        descricao="Troca do óleo do motor",
        preco=Decimal("150.00"),
        tempo_estimado_minutos=30,
    )

    assert servico.nome == "Troca de óleo"
    assert servico.preco == Decimal("150.00")
    assert servico.ativo is True


def test_rejeitar_preco_negativo_no_servico():
    with pytest.raises(ValueError):
        Servico(
            nome="Troca de óleo",
            descricao="Troca do óleo",
            preco=Decimal("-10.00"),
            tempo_estimado_minutos=30,
        )


def test_criar_peca():
    peca = Peca(
        nome="Filtro de óleo",
        preco=Decimal("40.00"),
        quantidade_estoque=10,
    )

    assert peca.quantidade_estoque == 10
    assert peca.preco == Decimal("40.00")


def test_retirar_peca_do_estoque():
    peca = Peca(
        nome="Filtro de óleo",
        preco=Decimal("40.00"),
        quantidade_estoque=10,
    )

    peca.retirar_estoque(3)

    assert peca.quantidade_estoque == 7


def test_impedir_estoque_negativo():
    peca = Peca(
        nome="Filtro de óleo",
        preco=Decimal("40.00"),
        quantidade_estoque=2,
    )

    with pytest.raises(ValueError, match="Estoque insuficiente"):
        peca.retirar_estoque(3)

    assert peca.quantidade_estoque == 2


def test_adicionar_pecas_ao_estoque():
    peca = Peca(
        nome="Filtro de óleo",
        preco=Decimal("40.00"),
        quantidade_estoque=2,
    )

    peca.adicionar_estoque(5)

    assert peca.quantidade_estoque == 7


def test_rejeitar_quantidade_negativa_no_estoque():
    with pytest.raises(ValueError):
        Peca(
            nome="Filtro de óleo",
            preco=Decimal("40.00"),
            quantidade_estoque=-1,
        )
