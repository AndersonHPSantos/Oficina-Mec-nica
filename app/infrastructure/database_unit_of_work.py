from contextlib import contextmanager

from app.infrastructure.database import database


class MongoUnitOfWork:

    @contextmanager
    def transacao(self):
        with database.client.start_session() as session:
            with session.start_transaction():
                yield session