
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.entities.item_os import ItemOS
from app.domain.enums.status_os import StatusOS, StatusOrcamento


@dataclass
class OrdemServico:
    # Atributos obrigatórios primeiro
    cliente_id: UUID
    veiculo_id: UUID

    # Atributos com valores padrão
    id: UUID = field(default_factory=uuid4)
    status: StatusOS = StatusOS.RECEBIDA
    status_orcamento: StatusOrcamento = StatusOrcamento.PENDENTE
    itens: list[ItemOS] = field(default_factory=list)
    valor_orcamento: Decimal = Decimal("0.00")

    def iniciar_diagnostico(self):
        if self.status != StatusOS.RECEBIDA:
            raise ValueError("Ordem de serviço não está no status RECEBIDA.")

        self.status = StatusOS.EM_DIAGNOSTICO

    def adicionar_item(self, item: ItemOS):
        if self.status != StatusOS.EM_DIAGNOSTICO:
            raise ValueError(
                "Só é possível adicionar itens durante o diagnóstico."
            )

        self.itens.append(item)

    @property
    def calcular_orcamento(self) -> Decimal:
        total = sum(
            (item.quantidade * item.preco_unitario for item in self.itens),
            Decimal("0.00")
        )

        return total

    def disponibilizar_orcamento(self, total_informado=None):
        if self.status != StatusOS.EM_DIAGNOSTICO:
            raise ValueError("Ordem não está em diagnóstico.")

        if not self.itens:
            raise ValueError("Não é possível gerar orçamento sem itens.")

        total_calculado = self.calcular_orcamento

        if (
            total_informado is not None
            and total_informado != total_calculado
        ):
            raise ValueError("O total informado está incorreto.")

        self.valor_orcamento = total_calculado
        self.status_orcamento = StatusOrcamento.DISPONIVEL

    def aprovar_orcamento(self):
        if self.status_orcamento != StatusOrcamento.DISPONIVEL:
            raise ValueError("Orçamento não está disponível para aprovação.")

        self.status_orcamento = StatusOrcamento.APROVADO

    def rejeitar_orcamento(self):
        if self.status_orcamento != StatusOrcamento.DISPONIVEL:
            raise ValueError("Orçamento não está disponível para rejeição.")

        self.status_orcamento = StatusOrcamento.REJEITADO

    def iniciar_execucao(self):
        if self.status_orcamento != StatusOrcamento.APROVADO:
            raise ValueError("Orçamento precisa estar aprovado.")

        self.status = StatusOS.EM_EXECUCAO

    def finalizar(self):
        if self.status != StatusOS.EM_EXECUCAO:
            raise ValueError("Ordem precisa estar em execução.")

        self.status = StatusOS.FINALIZADA

    def entregar(self):
        if self.status != StatusOS.FINALIZADA:
            raise ValueError("Ordem precisa estar finalizada.")

        self.status = StatusOS.ENTREGUE
