import pytest

from app.domain.value_objects.documento import Documento


def test_cpf_valido():
    documento = Documento("529.982.247-25")

    assert documento.valor == "52998224725"
    assert documento.tipo == "CPF"


def test_cnpj_valido():
    documento = Documento("11.222.333/0001-81")

    assert documento.valor == "11222333000181"
    assert documento.tipo == "CNPJ"


def test_documento_invalido():
    with pytest.raises(ValueError):
        Documento("111.111.111-11")


def test_documento_com_tamanho_invalido():
    with pytest.raises(ValueError):
        Documento("123456")