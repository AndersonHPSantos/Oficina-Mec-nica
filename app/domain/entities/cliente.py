from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.value_objects.documento import Documento

@dataclass
class Cliente:
    nome: str
    email: str
    documento: str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.nome = self.nome.strip()
        self.email = self.email.strip().lower()

        if not self.nome:
            raise ValueError("Nome do cliente é obrigatório")
        if not self.email:
            raise ValueError("E-mail do cliente é obrigatório")