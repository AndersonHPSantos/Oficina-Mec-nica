from uuid import UUID

from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class IniciarExecucao:

    def __init__(self, ordens, pecas, unidade_trabalho):
        self.ordens = ordens
        self.pecas = pecas
        self.unidade_trabalho = unidade_trabalho

    def executar(self, ordem_id: str):

        try:
            id_uuid = UUID(ordem_id)
        except ValueError:
            raise ValueError("ID da Ordem de Serviço inválido.")

        with self.unidade_trabalho.transacao() as session:

            ordem = self.ordens.buscar_por_id(
                id_uuid,
                session=session,
            )

            if ordem is None:
                raise ValueError("Ordem de Serviço não encontrada.")

            # Valida se o orçamento foi aprovado e se a OS
            # pode entrar em execução.
            ordem.iniciar_execucao()

            # Agrupa as quantidades por peça.
            pecas_necessarias = {}

            for item in ordem.itens:
                if item.tipo == "peca":
                    referencia = item.referencia_id

                    pecas_necessarias[referencia] = (
                        pecas_necessarias.get(referencia, 0)
                        + item.quantidade
                    )

            # Realiza a baixa de todas as peças.
            for peca_id, quantidade in pecas_necessarias.items():

                estoque_baixado = self.pecas.baixar_estoque(
                    peca_id,
                    quantidade,
                    session=session,
                )

                if not estoque_baixado:
                    raise ValueError(
                        f"Estoque insuficiente para a peça {peca_id}."
                    )

            # Persiste a OS dentro da mesma transação.
            self.ordens.salvar(
                ordem,
                session=session,
            )

            return ordem