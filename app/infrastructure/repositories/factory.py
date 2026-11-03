from app.infrastructure.database import database
from app.infrastructure.repositories.mongo_cliente_repository import (
    MongoClienteRepository,
)


from app.infrastructure.database import database
from app.infrastructure.repositories.mongo_cliente_repository import (
    MongoClienteRepository,
)
from app.infrastructure.repositories.mongo_veiculo_repository import (
    MongoVeiculoRepository,
)


def criar_repositorio_clientes() -> MongoClienteRepository:
    return MongoClienteRepository(database["clientes"])


def criar_repositorio_veiculos() -> MongoVeiculoRepository:
    return MongoVeiculoRepository(database["veiculos"])



def criar_repositorio_clientes() -> MongoClienteRepository:
    return MongoClienteRepository(database["clientes"])
