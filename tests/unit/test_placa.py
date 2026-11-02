
import pytest

from app.domain.value_objects.placa import Placa


def test_placa_antiga():
    placa = Placa("ABC-1234")

    assert placa.valor == "ABC1234"


def test_placa_mercosul():
    placa = Placa("ABC1D23")

    assert placa.valor == "ABC1D23"


def test_placa_invalida():
    with pytest.raises(ValueError):
        Placa("123-ABCD")
