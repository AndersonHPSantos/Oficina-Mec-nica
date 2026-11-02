
import pytest
from decimal import Decimal

from app.domain.entities.servico import Servico
from app.domain.entities.peca import Peca
from app.domain.entities.item_os import ItemOS


def test_criar_servico():
    servico = Servico(
        nome=" Troca de óleo ",
        descricao="Troca de óleo do motor",
        preco=Decimal("150.00"),
        tempo_estimado_minutos=45
    )

    assert servico.nome == "Troca de óleo"
    assert servico.preco == Decimal("150.00")
    assert servico.ativo is True


def test_rejeitar_preco_negativo_no_servico():
    with pytest.raises(ValueError):
        Servico(
            nome="Alinhamento",
            descricao="Alinhamento de rodas",
            preco=Decimal("-10.00"),
            tempo_estimado_minutos=30
        )


def test_retirar_estoque():
    peca = Peca(
        nome="Filtro de óleo",
        preco=Decimal("40.00"),
        quantidade_estoque=10
    )

    peca.retirar_estoque(3)

    assert peca.quantidade_estoque == 7


def test_impedir_estoque_negativo():
    peca = Peca(
        nome="Filtro de óleo",
        preco=Decimal("40.00"),
        quantidade_estoque=2
    )

    with pytest.raises(ValueError):
        peca.retirar_estoque(3)

    assert peca.quantidade_estoque == 2


def test_calcular_subtotal_do_item():
    servico = ItemOS(
        descricao="Alinhamento",
        quantidade=2,
        preco_unitario=Decimal("80.00"),
        tipo="servico",
        referencia_id=__import__("uuid").uuid4()
    )

    assert servico.subtotal == Decimal("160.00")


def test_rejeitar_quantidade_zero():
    with pytest.raises(ValueError):
        ItemOS(
            descricao="Filtro",
            quantidade=0,
            preco_unitario=Decimal("40.00"),
            tipo="peca",
            referencia_id=__import__("uuid").uuid4()
        )
