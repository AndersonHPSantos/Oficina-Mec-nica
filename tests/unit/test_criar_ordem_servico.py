
from uuid import uuid4

import pytest

from app.application.use_cases.ordens_servico.criar_ordem_servico import (
    CriarOrdemServico,
)
from app.domain.entities.cliente import Cliente
from app.domain.entities.veiculo import Veiculo
from app.domain.value_objects.documento import Documento
from app.domain.value_objects.placa import Placa


class ClientesFalsos:
    def __init__(self, cliente):
        self.cliente = cliente

    def buscar_por_id(self, cliente_id):
        if self.cliente.id == cliente_id:
            return self.cliente
        return None


class VeiculosFalsos:
    def __init__(self, veiculo):
        self.veiculo = veiculo

    def buscar_por_id(self, veiculo_id):
        if self.veiculo.id == veiculo_id:
            return self.veiculo
        return None


class OrdensFalsas:
    def __init__(self):
        self.ordens = []

    def salvar(self, ordem):
        self.ordens.append(ordem)
        return ordem


@pytest.fixture
def dependencias():
    cliente = Cliente(
        nome="João da Silva",
        email="joao@example.com",
        documento=Documento("529.982.247-25"),
    )

    veiculo = Veiculo(
        cliente_id=cliente.id,
        placa=Placa("ABC1D23"),
        marca="Volkswagen",
        modelo="Gol",
        ano=2020,
    )

    clientes = ClientesFalsos(cliente)
    veiculos = VeiculosFalsos(veiculo)
    ordens = OrdensFalsas()

    caso_de_uso = CriarOrdemServico(
        clientes=clientes,
        veiculos=veiculos,
        ordens=ordens,
    )

    return cliente, veiculo, ordens, caso_de_uso


def test_criar_ordem_servico(dependencias):
    cliente, veiculo, ordens, caso_de_uso = dependencias

    ordem = caso_de_uso.executar(
        cliente_id=str(cliente.id),
        veiculo_id=str(veiculo.id),
    )

    assert ordem.cliente_id == cliente.id
    assert ordem.veiculo_id == veiculo.id
    assert len(ordens.ordens) == 1


def test_impedir_os_para_cliente_inexistente(dependencias):
    _, veiculo, ordens, caso_de_uso = dependencias

    with pytest.raises(ValueError, match="Cliente não encontrado"):
        caso_de_uso.executar(
            cliente_id=str(uuid4()),
            veiculo_id=str(veiculo.id),
        )

    assert ordens.ordens == []


def test_impedir_os_para_veiculo_inexistente(dependencias):
    cliente, _, ordens, caso_de_uso = dependencias

    with pytest.raises(ValueError, match="Veículo não encontrado"):
        caso_de_uso.executar(
            cliente_id=str(cliente.id),
            veiculo_id=str(uuid4()),
        )

    assert ordens.ordens == []


def test_impedir_veiculo_de_outro_cliente(dependencias):
    cliente, veiculo, ordens, caso_de_uso = dependencias

    outro_cliente = Cliente(
        nome="Maria da Silva",
        email="maria@example.com",
        documento=Documento("111.444.777-35"),
    )

    # O repositório de clientes precisa reconhecer o segundo cliente.
    caso_de_uso.clientes.cliente = outro_cliente

    with pytest.raises(ValueError, match="não pertence"):
        caso_de_uso.executar(
            cliente_id=str(outro_cliente.id),
            veiculo_id=str(veiculo.id),
        )

    assert ordens.ordens == []
