
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Servico:
    nome: str
    descricao: str
    preco: Decimal
    tempo_estimado_minutos: int
    id: UUID = field(default_factory=uuid4)
    ativo: bool = True

    def __post_init__(self):
        self.nome = self.nome.strip()
        self.descricao = self.descricao.strip()
        self.preco = Decimal(str(self.preco))

        if not self.nome:
            raise ValueError("O nome do serviço é obrigatório")

        if not self.preco.is_finite() or self.preco < 0:
            raise ValueError("O preço do serviço não pode ser negativo")

        self.preco = self.preco.quantize(Decimal("0.01"))

        if self.tempo_estimado_minutos <= 0:
            raise ValueError(
                "O tempo estimado deve ser maior que zero"
            )
