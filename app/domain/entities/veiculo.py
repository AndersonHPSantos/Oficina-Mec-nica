from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.value_objects.placa import Placa

@dataclass
class Veiculo:
    cliente_id: UUID
    placa: Placa
    marca: str
    modelo: str
    ano: int
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.marca = self.marca.strip()
        self.modelo = self.modelo.strip()

        if not self.marca or not self.modelo:
            raise ValueError("Marca e modelo são obrigatórios")

        if self.ano < 1886:
            raise ValueError("Ano de fabricação inválido")