
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.entities.item_os import ItemOS
from app.domain.enums.status_os import StatusOS, StatusOrcamento


@dataclass
class OrdemServico:
    # Campos obrigatórios primeiro
    cliente_id: UUID
    veiculo_id: UUID

    # Campos com valores padrão
    id: UUID = field(default_factory=uuid4)

    itens: list[ItemOS] = field(default_factory=list)

    status: StatusOS = StatusOS.RECEBIDA
    status_orcamento: StatusOrcamento = StatusOrcamento.PENDENTE

    valor_orcamento: Decimal = Decimal("0.00")

    criada_em: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    diagnostico_em: datetime | None = None
    iniciada_em: datetime | None = None
    finalizada_em: datetime | None = None
    entregue_em: datetime | None = None

    def iniciar_diagnostico(self):
        if self.status != StatusOS.RECEBIDA:
            raise ValueError(
                "A OS precisa estar recebida para iniciar o diagnóstico"
            )

        self.status = StatusOS.EM_DIAGNOSTICO
        self.diagnostico_em = datetime.now(timezone.utc)

    def adicionar_item(self, item: ItemOS):
        if self.status != StatusOS.EM_DIAGNOSTICO:
            raise ValueError(
                "Só é possível adicionar itens durante o diagnóstico"
            )

        if not isinstance(item, ItemOS):
            raise ValueError("O item informado é inválido")

        self.itens.append(item)

    @property
    def calcular_orcamento(self) -> Decimal:
        total = sum(
            (item.subtotal for item in self.itens),
            Decimal("0.00")
        )

        return total.quantize(Decimal("0.01"))

    def disponibilizar_orcamento(
        self,
        valor: Decimal | None = None
    ):
        if self.status != StatusOS.EM_DIAGNOSTICO:
            raise ValueError(
                "A OS precisa estar em diagnóstico"
            )

        total = self.calcular_orcamento

        if not self.itens:
            raise ValueError(
                "Adicione ao menos um serviço ou peça ao orçamento"
            )

        if valor is not None and Decimal(str(valor)) != total:
            raise ValueError(
                "O valor informado diverge da soma dos itens"
            )

        self.valor_orcamento = total
        self.status_orcamento = StatusOrcamento.PENDENTE
        self.status = StatusOS.AGUARDANDO_APROVACAO

    def aprovar_orcamento(self):
        if self.status != StatusOS.AGUARDANDO_APROVACAO:
            raise ValueError(
                "A OS não está aguardando aprovação"
            )

        if self.status_orcamento != StatusOrcamento.PENDENTE:
            raise ValueError(
                "O orçamento não está pendente"
            )

        self.status_orcamento = StatusOrcamento.APROVADO

    def rejeitar_orcamento(self):
        if self.status != StatusOS.AGUARDANDO_APROVACAO:
            raise ValueError(
                "A OS não está aguardando aprovação"
            )

        if self.status_orcamento != StatusOrcamento.PENDENTE:
            raise ValueError(
                "O orçamento não está pendente"
            )

        self.status_orcamento = StatusOrcamento.REJEITADO

    def iniciar_execucao(self):
        if self.status != StatusOS.AGUARDANDO_APROVACAO:
            raise ValueError(
                "A OS não está aguardando aprovação"
            )

        if self.status_orcamento != StatusOrcamento.APROVADO:
            raise ValueError(
                "O orçamento precisa estar aprovado"
            )

        self.status = StatusOS.EM_EXECUCAO
        self.iniciada_em = datetime.now(timezone.utc)

    def finalizar(self):
        if self.status != StatusOS.EM_EXECUCAO:
            raise ValueError(
                "Somente uma OS em execução pode ser finalizada"
            )

        self.status = StatusOS.FINALIZADA
        self.finalizada_em = datetime.now(timezone.utc)

    def entregar(self):
        if self.status != StatusOS.FINALIZADA:
            raise ValueError(
                "Somente uma OS finalizada pode ser entregue"
            )

        self.status = StatusOS.ENTREGUE
        self.entregue_em = datetime.now(timezone.utc)
