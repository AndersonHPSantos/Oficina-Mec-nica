from app.infrastructure.database import database
from app.infrastructure.repositories.mongo_cliente_repository import (
    MongoClienteRepository,
)


def criar_repositorio_clientes() -> MongoClienteRepository:
    return MongoClienteRepository(database["clientes"])
