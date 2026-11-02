
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Documento:
    valor: str

    def __post_init__(self):
        documento = re.sub(r"\D", "", self.valor)

        if len(documento) == 11:
            if not self._validar_cpf(documento):
                raise ValueError("CPF inválido")

        elif len(documento) == 14:
            if not self._validar_cnpj(documento):
                raise ValueError("CNPJ inválido")

        else:
            raise ValueError("Documento deve ser CPF ou CNPJ")

        object.__setattr__(self, "valor", documento)

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        if cpf == cpf[0] * 11:
            return False

        numeros = [int(n) for n in cpf]

        soma = sum(numeros[i] * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10

        if digito1 != numeros[9]:
            return False

        soma = sum(numeros[i] * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10

        return digito2 == numeros[10]

    @staticmethod
    def _validar_cnpj(cnpj: str) -> bool:
        if cnpj == cnpj[0] * 14:
            return False

        numeros = [int(n) for n in cnpj]

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(a * b for a, b in zip(numeros[:12], pesos1))

        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        if digito1 != numeros[12]:
            return False

        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(a * b for a, b in zip(numeros[:13], pesos2))

        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return digito2 == numeros[13]

    @property
    def tipo(self) -> str:
        return "CPF" if len(self.valor) == 11 else "CNPJ"
