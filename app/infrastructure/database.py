from pymongo import MongoClient

from app.core.config import settings

client = MongoClient(
    settings.MONGODB_URI,
    serverSelectionTimeoutMS = 3000
)

database = client[settings.MONGODB_DATABASE]

def verificar_conexao() -> bool:
    client.admin.command("ping")
    return True