import pytest
from uuid import uuid4

from app.infrastructure.database import database


@pytest.fixture
def colecao_teste():
    nome = f"teste_transacao_{uuid4().hex}"
    colecao = database[nome]

    yield colecao

    colecao.drop()


def test_transacao_desfaz_alteracoes_apos_falha(colecao_teste):
    colecao_teste.insert_one({
        "id": "peca-1",
        "quantidade_estoque": 5,
    })

    with pytest.raises(RuntimeError):
        with database.client.start_session() as session:
            with session.start_transaction():
                colecao_teste.update_one(
                    {"id": "peca-1"},
                    {"$inc": {"quantidade_estoque": -2}},
                    session=session,
                )

                # Simula uma falha depois da primeira alteração.
                raise RuntimeError("Falha simulada")

    documento = colecao_teste.find_one({"id": "peca-1"})

    assert documento["quantidade_estoque"] == 5