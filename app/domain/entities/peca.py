
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Peca:
    nome: str
    preco: Decimal
    quantidade_estoque: int
    id: UUID = field(default_factory=uuid4)
    ativa: bool = True

    def __post_init__(self):
        self.nome = self.nome.strip()
        self.preco = Decimal(str(self.preco))

        if not self.nome:
            raise ValueError("O nome da peça é obrigatório")

        if not self.preco.is_finite() or self.preco < 0:
            raise ValueError("O preço da peça não pode ser negativo")

        self.preco = self.preco.quantize(Decimal("0.01"))

        if (
            isinstance(self.quantidade_estoque, bool)
            or not isinstance(self.quantidade_estoque, int)
            or self.quantidade_estoque < 0
        ):
            raise ValueError("A quantidade em estoque é inválida")

    def retirar_estoque(self, quantidade: int):
        if (
            isinstance(quantidade, bool)
            or not isinstance(quantidade, int)
            or quantidade <= 0
        ):
            raise ValueError("A quantidade deve ser um inteiro positivo")

        if quantidade > self.quantidade_estoque:
            raise ValueError("Estoque insuficiente")

        self.quantidade_estoque -= quantidade

    def adicionar_estoque(self, quantidade: int):
        if (
            isinstance(quantidade, bool)
            or not isinstance(quantidade, int)
            or quantidade <= 0
        ):
            raise ValueError("A quantidade deve ser um inteiro positivo")

        self.quantidade_estoque += quantidade
