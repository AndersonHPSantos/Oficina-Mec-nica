
from decimal import Decimal

from app.domain.entities.peca import Peca
from app.domain.repositories.peca_repository import PecaRepository


class CadastrarPeca:

    def __init__(self, repositorio: PecaRepository):
        self.repositorio = repositorio

    def executar(
        self,
        nome: str,
        preco: Decimal,
        quantidade_estoque: int,
    ) -> Peca:
        peca = Peca(
            nome=nome,
            preco=preco,
            quantidade_estoque=quantidade_estoque,
        )
        return self.repositorio.salvar(peca)
