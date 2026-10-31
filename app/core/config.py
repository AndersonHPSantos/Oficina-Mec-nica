import os

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Oficina API")
    APP_ENV = os.getenv("APP_ENV", "development")

    MONGODB_URI = os.getenv(
        "MONGODB_URI",
        "mongodb://localhost:27017"
    )
    MONGODB_DATABASE = os.getenv(
        "MONGODB_DATABASE",
        "oficina_db"
    )
    JWT_SECRET = os.getenv("JWT_SECRET", "")
    JWS_EXPIRE_MINUTES = int(
        os.getenv("JWT_EXPIRE_MINUTES", 30)
    )

settings = Settings()