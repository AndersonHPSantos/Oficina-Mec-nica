
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.application.use_cases.ordens_servico.criar_ordem_servico import (
    CriarOrdemServico,
)
from app.infrastructure.repositories.factory import (
    criar_repositorio_clientes,
    criar_repositorio_veiculos,
    criar_repositorio_ordens,
    criar_unidade_trabalho
)

router = APIRouter(prefix="/ordens-servico", tags=["Ordens de Serviço"])


class CriarOrdemEntrada(BaseModel):
    cliente_id: str
    veiculo_id: str


class OrdemResposta(BaseModel):
    id: str
    cliente_id: str
    veiculo_id: str
    status: str
    status_orcamento: str
    valor_orcamento: str


def converter_ordem(ordem) -> OrdemResposta:
    return OrdemResposta(
        id=str(ordem.id),
        cliente_id=str(ordem.cliente_id),
        veiculo_id=str(ordem.veiculo_id),
        status=ordem.status.value,
        status_orcamento=ordem.status_orcamento.value,
        valor_orcamento=str(ordem.valor_orcamento),
    )


@router.post("", response_model=OrdemResposta, status_code=201)
def criar_ordem(entrada: CriarOrdemEntrada):
    caso_de_uso = CriarOrdemServico(
        clientes=criar_repositorio_clientes(),
        veiculos=criar_repositorio_veiculos(),
        ordens=criar_repositorio_ordens(),
    )

    try:
        ordem = caso_de_uso.executar(
            cliente_id=entrada.cliente_id,
            veiculo_id=entrada.veiculo_id,
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_ordem(ordem)



from pydantic import BaseModel, Field

from app.application.use_cases.ordens_servico.adicionar_item import (
    AdicionarItemOS,
)
from app.application.use_cases.ordens_servico.disponibilizar_orcamento import (
    DisponibilizarOrcamento,
)
from app.application.use_cases.ordens_servico.decidir_orcamento import (
    DecidirOrcamento,
)
from app.application.use_cases.ordens_servico.iniciar_diagnostico import (
    IniciarDiagnostico,
)
from app.infrastructure.repositories.factory import (
    criar_repositorio_servicos,
    criar_repositorio_pecas,
)




class ItemOSEntrada(BaseModel):
    tipo: str
    referencia_id: str
    quantidade: int = Field(default=1, ge=1)


class DecisaoOrcamentoEntrada(BaseModel):
    aprovado: bool


@router.post("/{ordem_id}/diagnostico", response_model=OrdemResposta)
def iniciar_diagnostico(ordem_id: str):
    try:
        ordem = IniciarDiagnostico(
            criar_repositorio_ordens()
        ).executar(ordem_id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_ordem(ordem)


@router.post("/{ordem_id}/itens", response_model=OrdemResposta)
def adicionar_item(ordem_id: str, entrada: ItemOSEntrada):
    try:
        ordem = AdicionarItemOS(
            ordens=criar_repositorio_ordens(),
            servicos=criar_repositorio_servicos(),
            pecas=criar_repositorio_pecas(),
        ).executar(
            ordem_id=ordem_id,
            tipo=entrada.tipo,
            referencia_id=entrada.referencia_id,
            quantidade=entrada.quantidade,
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_ordem(ordem)


@router.post(
    "/{ordem_id}/disponibilizar-orcamento",
    response_model=OrdemResposta,
)
def disponibilizar_orcamento(ordem_id: str):
    try:
        ordem = DisponibilizarOrcamento(
            criar_repositorio_ordens()
        ).executar(ordem_id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_ordem(ordem)


@router.post("/{ordem_id}/decisao-orcamento", response_model=OrdemResposta)
def decidir_orcamento(
    ordem_id: str,
    entrada: DecisaoOrcamentoEntrada,
):
    try:
        ordem = DecidirOrcamento(
            criar_repositorio_ordens()
        ).executar(
            ordem_id=ordem_id,
            aprovado=entrada.aprovado,
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    return converter_ordem(ordem)


from app.application.use_cases.ordens_servico.iniciar_execucao import (
    IniciarExecucao,
)
from app.application.use_cases.ordens_servico.finalizar_ordem_servico import (
    FinalizarOrdemServico,
)
from app.application.use_cases.ordens_servico.entregar_ordem_servico import (
    EntregarOrdemServico,
)
'''
@router.post("/{ordem_id}/iniciar-execucao", response_model=OrdemResposta)
def iniciar_execucao(ordem_id: str):
    caso_de_uso = IniciarExecucao(criar_repositorio_ordens())

    try:
        ordem = caso_de_uso.executar(ordem_id)
        return converter_ordem(ordem)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
'''

@router.post("/{ordem_id}/iniciar-execucao", response_model=OrdemResposta)
def iniciar_execucao(ordem_id: str):

    caso_de_uso = IniciarExecucao(
        criar_repositorio_ordens(),
        criar_repositorio_pecas(),
        criar_unidade_trabalho(),
    )

    try:
        ordem = caso_de_uso.executar(ordem_id)
        return converter_ordem(ordem)

    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))

@router.post("/{ordem_id}/finalizar", response_model=OrdemResposta)
def finalizar_ordem(ordem_id: str):
    caso_de_uso = FinalizarOrdemServico(criar_repositorio_ordens())

    try:
        ordem = caso_de_uso.executar(ordem_id)
        return converter_ordem(ordem)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.post("/{ordem_id}/entregar", response_model=OrdemResposta)
def entregar_ordem(ordem_id: str):
    caso_de_uso = EntregarOrdemServico(criar_repositorio_ordens())

    try:
        ordem = caso_de_uso.executar(ordem_id)
        return converter_ordem(ordem)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))