from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.application.use_cases.clientes.cadastrar_cliente import (
    CadastrarCliente,
)
from app.application.use_cases.clientes.buscar_cliente import BuscarCliente
from app.application.use_cases.clientes.listar_clientes import ListarClientes
from app.infrastructure.repositories.factory import (
    criar_repositorio_clientes,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


class ClienteEntrada(BaseModel):
    nome: str
    email: EmailStr
    documento: str


class ClienteResposta(BaseModel):
    id: str
    nome: str
    email: str
    documento: str


def converter_cliente(cliente) -> ClienteResposta:
    return ClienteResposta(
        id=str(cliente.id),
        nome=cliente.nome,
        email=cliente.email,
        documento=cliente.documento.valor,
    )


@router.post("", response_model=ClienteResposta, status_code=201)
def cadastrar_cliente(entrada: ClienteEntrada):
    repositorio = criar_repositorio_clientes()
    caso_de_uso = CadastrarCliente(repositorio)

    try:
        cliente = caso_de_uso.executar(
            nome=entrada.nome,
            email=str(entrada.email),
            documento=entrada.documento,
        )
        return converter_cliente(cliente)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro


@router.get("", response_model=list[ClienteResposta])
def listar_clientes():
    repositorio = criar_repositorio_clientes()
    clientes = ListarClientes(repositorio).executar()
    return [converter_cliente(cliente) for cliente in clientes]


@router.get("/{cliente_id}", response_model=ClienteResposta)
def buscar_cliente(cliente_id: str):
    repositorio = criar_repositorio_clientes()

    try:
        cliente = BuscarCliente(repositorio).executar(cliente_id)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )

    return converter_cliente(cliente)
