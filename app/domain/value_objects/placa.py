from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Placa:
    valor: str

    def __post_init__(self):
        placa = re.sub(r"[^A-Z0-9]", "", self.valor.upper())

        # Padrão antigo -> ABC-1234
        padrao_antigo = r"[A-Z]{3}[0-9]{4}$"

        # Padrão Merco sul -> ABC1D23
        padrao_mercosul = r"[A-Z]{3}[0-9][A-Z][0-9]{2}$"

        if not (
            re.fullmatch(padrao_antigo, placa) or
            re.fullmatch(padrao_mercosul, placa)
        ):
            raise ValueError("Placa de veículo inválida")

        object.__setattr__(self, "valor", placa)