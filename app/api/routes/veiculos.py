
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.application.use_cases.veiculos.cadastrar_veiculo import (
    CadastrarVeiculo,
)
from app.infrastructure.repositories.factory import (
    criar_repositorio_clientes,
    criar_repositorio_veiculos,
)

router = APIRouter(prefix="/veiculos", tags=["Veículos"])


class VeiculoEntrada(BaseModel):
    cliente_id: str
    placa: str
    marca: str
    modelo: str
    ano: int = Field(ge=1886, le=2100)


class VeiculoResposta(BaseModel):
    id: str
    cliente_id: str
    placa: str
    marca: str
    modelo: str
    ano: int


def converter_veiculo(veiculo) -> VeiculoResposta:
    return VeiculoResposta(
        id=str(veiculo.id),
        cliente_id=str(veiculo.cliente_id),
        placa=veiculo.placa.valor,
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        ano=veiculo.ano,
    )


@router.post("", response_model=VeiculoResposta, status_code=201)
def cadastrar_veiculo(entrada: VeiculoEntrada):
    clientes = criar_repositorio_clientes()
    veiculos = criar_repositorio_veiculos()

    caso_de_uso = CadastrarVeiculo(clientes, veiculos)

    try:
        veiculo = caso_de_uso.executar(
            cliente_id=entrada.cliente_id,
            placa=entrada.placa,
            marca=entrada.marca,
            modelo=entrada.modelo,
            ano=entrada.ano,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro

    return converter_veiculo(veiculo)


@router.get("/cliente/{cliente_id}", response_model=list[VeiculoResposta])
def listar_veiculos_do_cliente(cliente_id: str):
    from uuid import UUID

    clientes = criar_repositorio_clientes()
    veiculos = criar_repositorio_veiculos()

    try:
        identificador = UUID(cliente_id)
    except (ValueError, TypeError, AttributeError) as erro:
        raise HTTPException(
            status_code=400,
            detail="Identificador do cliente inválido",
        ) from erro

    if clientes.buscar_por_id(identificador) is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado",
        )

    resultado = veiculos.listar_por_cliente(identificador)

    return [converter_veiculo(veiculo) for veiculo in resultado]
