
from uuid import uuid4

import pytest

from app.application.use_cases.veiculos.cadastrar_veiculo import (
    CadastrarVeiculo,
)
from app.domain.entities.cliente import Cliente
from app.domain.entities.veiculo import Veiculo
from app.domain.value_objects.documento import Documento


class ClientesFalsos:

    def __init__(self):
        self.clientes = {}

    def salvar(self, cliente):
        self.clientes[cliente.id] = cliente
        return cliente

    def buscar_por_id(self, cliente_id):
        return self.clientes.get(cliente_id)

    def buscar_por_documento(self, documento):
        return next(
            (
                c for c in self.clientes.values()
                if c.documento.valor == documento
            ),
            None,
        )

    def listar(self):
        return list(self.clientes.values())


class VeiculosFalsos:

    def __init__(self):
        self.veiculos = []

    def salvar(self, veiculo):
        if self.buscar_por_placa(veiculo.placa.valor):
            raise ValueError("Já existe um veículo com essa placa")
        self.veiculos.append(veiculo)
        return veiculo

    def buscar_por_id(self, veiculo_id):
        return next(
            (v for v in self.veiculos if v.id == veiculo_id),
            None,
        )

    def buscar_por_placa(self, placa):
        return next(
            (v for v in self.veiculos if v.placa.valor == placa),
            None,
        )

    def listar_por_cliente(self, cliente_id):
        return [
            v for v in self.veiculos
            if v.cliente_id == cliente_id
        ]


@pytest.fixture
def dependencias():
    clientes = ClientesFalsos()
    veiculos = VeiculosFalsos()

    cliente = Cliente(
        nome="João da Silva",
        email="joao@example.com",
        documento=Documento("529.982.247-25"),
    )
    clientes.salvar(cliente)

    caso_de_uso = CadastrarVeiculo(clientes, veiculos)

    return cliente, veiculos, caso_de_uso


def test_cadastrar_veiculo(dependencias):
    cliente, veiculos, caso_de_uso = dependencias

    veiculo = caso_de_uso.executar(
        cliente_id=str(cliente.id),
        placa="ABC1D23",
        marca="Volkswagen",
        modelo="Gol",
        ano=2020,
    )

    assert veiculo.cliente_id == cliente.id
    assert veiculo.placa.valor == "ABC1D23"
    assert len(veiculos.listar_por_cliente(cliente.id)) == 1


def test_impedir_veiculo_de_cliente_inexistente(dependencias):
    _, _, caso_de_uso = dependencias

    with pytest.raises(ValueError, match="cliente não existe"):
        caso_de_uso.executar(
            cliente_id=str(uuid4()),
            placa="ABC1D23",
            marca="Volkswagen",
            modelo="Gol",
            ano=2020,
        )


def test_impedir_placa_invalida(dependencias):
    cliente, _, caso_de_uso = dependencias

    with pytest.raises(ValueError, match="Placa"):
        caso_de_uso.executar(
            cliente_id=str(cliente.id),
            placa="123-ABCD",
            marca="Volkswagen",
            modelo="Gol",
            ano=2020,
        )


def test_impedir_placa_duplicada(dependencias):
    cliente, _, caso_de_uso = dependencias

    dados = {
        "cliente_id": str(cliente.id),
        "placa": "ABC1D23",
        "marca": "Volkswagen",
        "modelo": "Gol",
        "ano": 2020,
    }

    caso_de_uso.executar(**dados)

    with pytest.raises(ValueError, match="placa"):
        caso_de_uso.executar(**dados)
