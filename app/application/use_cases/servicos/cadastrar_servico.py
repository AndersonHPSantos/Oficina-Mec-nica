
from decimal import Decimal

from app.domain.entities.servico import Servico
from app.domain.repositories.servico_repository import ServicoRepository


class CadastrarServico:

    def __init__(self, repositorio: ServicoRepository):
        self.repositorio = repositorio

    def executar(
        self,
        nome: str,
        descricao: str,
        preco: Decimal,
        tempo_estimado_minutos: int,
    ) -> Servico:
        servico = Servico(
            nome=nome,
            descricao=descricao,
            preco=preco,
            tempo_estimado_minutos=tempo_estimado_minutos,
        )
        return self.repositorio.salvar(servico)
