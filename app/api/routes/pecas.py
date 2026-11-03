
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.application.use_cases.pecas.cadastrar_peca import CadastrarPeca
from app.infrastructure.repositories.factory import criar_repositorio_pecas

router = APIRouter(prefix="/pecas", tags=["Peças"])


class PecaEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    preco: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    quantidade_estoque: int = Field(ge=0)


class PecaResposta(BaseModel):
    id: str
    nome: str
    preco: Decimal
    quantidade_estoque: int
    ativa: bool


def converter_peca(peca) -> PecaResposta:
    return PecaResposta(
        id=str(peca.id),
        nome=peca.nome,
        preco=peca.preco,
        quantidade_estoque=peca.quantidade_estoque,
        ativa=peca.ativa,
    )


@router.post("", response_model=PecaResposta, status_code=201)
def cadastrar_peca(entrada: PecaEntrada):
    repositorio = criar_repositorio_pecas()

    try:
        peca = CadastrarPeca(repositorio).executar(
            nome=entrada.nome,
            preco=entrada.preco,
            quantidade_estoque=entrada.quantidade_estoque,
        )
    except (ValueError, ArithmeticError) as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_peca(peca)


@router.get("", response_model=list[PecaResposta])
def listar_pecas():
    pecas = criar_repositorio_pecas().listar()
    return [converter_peca(peca) for peca in pecas]


@router.get("/{peca_id}", response_model=PecaResposta)
def buscar_peca(peca_id: str):
    try:
        identificador = UUID(peca_id)
    except (ValueError, TypeError, AttributeError) as erro:
        raise HTTPException(
            status_code=400,
            detail="Identificador da peça inválido",
        ) from erro

    peca = criar_repositorio_pecas().buscar_por_id(identificador)

    if peca is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")

    return converter_peca(peca)
