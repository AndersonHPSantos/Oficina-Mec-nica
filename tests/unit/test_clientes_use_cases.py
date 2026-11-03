
from uuid import uuid4

import pytest

from app.application.use_cases.clientes.buscar_cliente import BuscarCliente
from app.application.use_cases.clientes.listar_clientes import ListarClientes
from app.application.use_cases.clientes.cadastrar_cliente import CadastrarCliente
from app.domain.entities.cliente import Cliente
from app.domain.value_objects.documento import Documento


class RepositorioClienteFalso:

    def __init__(self):
        self.clientes = []

    def salvar(self, cliente):
        self.clientes.append(cliente)
        return cliente

    def buscar_por_id(self, cliente_id):
        return next(
            (c for c in self.clientes if c.id == cliente_id),
            None,
        )

    def buscar_por_documento(self, documento):
        return next(
            (
                c for c in self.clientes
                if c.documento.valor == documento
            ),
            None,
        )

    def listar(self):
        return list(self.clientes)


def test_cadastrar_cliente():
    repositorio = RepositorioClienteFalso()
    caso_de_uso = CadastrarCliente(repositorio)

    cliente = caso_de_uso.executar(
        nome="João da Silva",
        email="joao@example.com",
        documento="529.982.247-25",
    )

    assert cliente.nome == "João da Silva"
    assert cliente.email == "joao@example.com"
    assert len(repositorio.listar()) == 1


def test_nao_cadastrar_documento_duplicado():
    repositorio = RepositorioClienteFalso()
    caso_de_uso = CadastrarCliente(repositorio)

    dados = {
        "nome": "João da Silva",
        "email": "joao@example.com",
        "documento": "529.982.247-25",
    }

    caso_de_uso.executar(**dados)

    with pytest.raises(ValueError, match="Já existe"):
        caso_de_uso.executar(
            nome="Maria da Silva",
            email="maria@example.com",
            documento="529.982.247-25",
        )


def test_buscar_cliente_por_id():
    repositorio = RepositorioClienteFalso()
    cliente = Cliente(
        nome="João da Silva",
        email="joao@example.com",
        documento=Documento("529.982.247-25"),
    )
    repositorio.salvar(cliente)

    resultado = BuscarCliente(repositorio).executar(str(cliente.id))

    assert resultado is not None
    assert resultado.id == cliente.id


def test_rejeitar_id_invalido():
    caso_de_uso = BuscarCliente(RepositorioClienteFalso())

    with pytest.raises(ValueError, match="Identificador"):
        caso_de_uso.executar("id-invalido")


def test_listar_clientes():
    repositorio = RepositorioClienteFalso()
    repositorio.salvar(
        Cliente(
            nome="João",
            email="joao@example.com",
            documento=Documento("529.982.247-25"),
        )
    )

    resultado = ListarClientes(repositorio).executar()

    assert len(resultado) == 1
    assert resultado[0].nome == "João"
