import pytest

from app.domain.entities.ordem_servico import OrdemServico
from app.domain.enums.status_os import StatusOS, StatusOrcamento


def criar_ordem_aprovada():
    ordem = OrdemServico(
        cliente_id=__import__("uuid").uuid4(),
        veiculo_id=__import__("uuid").uuid4(),
    )

    # Prepara a entidade para testar as transições posteriores.
    ordem.status = StatusOS.AGUARDANDO_APROVACAO
    ordem.status_orcamento = StatusOrcamento.APROVADO

    return ordem


def test_iniciar_execucao():
    ordem = criar_ordem_aprovada()

    ordem.iniciar_execucao()

    assert ordem.status == StatusOS.EM_EXECUCAO
    assert ordem.iniciada_em is not None


def test_finalizar_ordem():
    ordem = criar_ordem_aprovada()
    ordem.iniciar_execucao()

    ordem.finalizar()

    assert ordem.status == StatusOS.FINALIZADA
    assert ordem.finalizada_em is not None


def test_entregar_ordem():
    ordem = criar_ordem_aprovada()
    ordem.iniciar_execucao()
    ordem.finalizar()

    ordem.entregar()

    assert ordem.status == StatusOS.ENTREGUE
    assert ordem.entregue_em is not None


def test_nao_permite_entregar_antes_de_finalizar():
    ordem = criar_ordem_aprovada()
    ordem.iniciar_execucao()

    with pytest.raises(ValueError):
        ordem.entregar()