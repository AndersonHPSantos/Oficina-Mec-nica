
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.application.use_cases.servicos.cadastrar_servico import CadastrarServico
from app.infrastructure.repositories.factory import criar_repositorio_servicos

router = APIRouter(prefix="/servicos", tags=["Serviços"])


class ServicoEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    descricao: str = Field(min_length=1, max_length=500)
    preco: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    tempo_estimado_minutos: int = Field(gt=0, le=100000)


class ServicoResposta(BaseModel):
    id: str
    nome: str
    descricao: str
    preco: Decimal
    tempo_estimado_minutos: int
    ativo: bool


def converter_servico(servico) -> ServicoResposta:
    return ServicoResposta(
        id=str(servico.id),
        nome=servico.nome,
        descricao=servico.descricao,
        preco=servico.preco,
        tempo_estimado_minutos=servico.tempo_estimado_minutos,
        ativo=servico.ativo,
    )


@router.post("", response_model=ServicoResposta, status_code=201)
def cadastrar_servico(entrada: ServicoEntrada):
    repositorio = criar_repositorio_servicos()

    try:
        servico = CadastrarServico(repositorio).executar(
            nome=entrada.nome,
            descricao=entrada.descricao,
            preco=entrada.preco,
            tempo_estimado_minutos=entrada.tempo_estimado_minutos,
        )
    except (ValueError, ArithmeticError) as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_servico(servico)


@router.get("", response_model=list[ServicoResposta])
def listar_servicos():
    servicos = criar_repositorio_servicos().listar()
    return [converter_servico(servico) for servico in servicos]


@router.get("/{servico_id}", response_model=ServicoResposta)
def buscar_servico(servico_id: str):
    from uuid import UUID

    try:
        identificador = UUID(servico_id)
    except (ValueError, TypeError, AttributeError) as erro:
        raise HTTPException(
            status_code=400,
            detail="Identificador do serviço inválido",
        ) from erro

    servico = criar_repositorio_servicos().buscar_por_id(identificador)

    if servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    return converter_servico(servico)
