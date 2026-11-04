
from uuid import UUID

from app.domain.entities.ordem_servico import OrdemServico
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.domain.repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)


class CriarOrdemServico:

    def __init__(
        self,
        clientes: ClienteRepository,
        veiculos: VeiculoRepository,
        ordens: OrdemServicoRepository,
    ):
        self.clientes = clientes
        self.veiculos = veiculos
        self.ordens = ordens

    def executar(
        self,
        cliente_id: str,
        veiculo_id: str,
    ) -> OrdemServico:
        try:
            identificador_cliente = UUID(cliente_id)
            identificador_veiculo = UUID(veiculo_id)
        except (ValueError, TypeError, AttributeError) as erro:
            raise ValueError(
                "Identificador de cliente ou veículo inválido"
            ) from erro

        cliente = self.clientes.buscar_por_id(identificador_cliente)

        if cliente is None:
            raise ValueError("Cliente não encontrado")

        veiculo = self.veiculos.buscar_por_id(identificador_veiculo)

        if veiculo is None:
            raise ValueError("Veículo não encontrado")

        if veiculo.cliente_id != identificador_cliente:
            raise ValueError(
                "O veículo informado não pertence ao cliente"
            )

        ordem = OrdemServico(
            cliente_id=identificador_cliente,
            veiculo_id=identificador_veiculo,
        )

        return self.ordens.salvar(ordem)
