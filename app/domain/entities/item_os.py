
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class ItemOS:
    descricao: str
    quantidade: int
    preco_unitario: Decimal
    tipo: str
    referencia_id: UUID

    def __post_init__(self):
        descricao = self.descricao.strip()
        preco = Decimal(str(self.preco_unitario))

        if not descricao:
            raise ValueError("A descrição do item é obrigatória")

        if (
            isinstance(self.quantidade, bool)
            or not isinstance(self.quantidade, int)
            or self.quantidade <= 0
        ):
            raise ValueError("A quantidade deve ser um inteiro positivo")

        if not preco.is_finite() or preco < 0:
            raise ValueError("O preço unitário não pode ser negativo")

        if self.tipo not in ("servico", "peca"):
            raise ValueError("Tipo deve ser 'servico' ou 'peca'")

        object.__setattr__(self, "descricao", descricao)
        object.__setattr__(
            self,
            "preco_unitario",
            preco.quantize(Decimal("0.01"))
        )

    @property
    def subtotal(self) -> Decimal:
        return (
            self.preco_unitario * self.quantidade
        ).quantize(Decimal("0.01"))
