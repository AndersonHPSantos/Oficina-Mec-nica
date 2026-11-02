from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Dinheiro:
    valor: Decimal

    def __post_init__(self):
        valor = Decimal(str(self.valor))

        if not valor.is_finite() or valor < 0:
            raise ValueError("Valor monetário inválido")

        object.__setattr__(
            self,
            "valor",
            valor.quantize(Decimal("0.01"))
        )

    def __add__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented

        return Dinheiro(self.valor + outro.valor)