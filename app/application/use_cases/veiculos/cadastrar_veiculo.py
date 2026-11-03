
from uuid import UUID

from app.domain.entities.veiculo import Veiculo
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.domain.value_objects.placa import Placa


class CadastrarVeiculo:

    def __init__(
        self,
        clientes: ClienteRepository,
        veiculos: VeiculoRepository,
    ):
        self.clientes = clientes
        self.veiculos = veiculos

    def executar(
        self,
        cliente_id: str,
        placa: str,
        marca: str,
        modelo: str,
        ano: int,
    ) -> Veiculo:
        try:
            identificador_cliente = UUID(cliente_id)
        except (ValueError, TypeError, AttributeError) as erro:
            raise ValueError("Identificador do cliente inválido") from erro

        cliente = self.clientes.buscar_por_id(identificador_cliente)

        if cliente is None:
            raise ValueError("O cliente não existe")

        placa_validada = Placa(placa)

        if self.veiculos.buscar_por_placa(placa_validada.valor):
            raise ValueError("Já existe um veículo com essa placa")

        veiculo = Veiculo(
            cliente_id=identificador_cliente,
            placa=placa_validada,
            marca=marca,
            modelo=modelo,
            ano=ano,
        )

        return self.veiculos.salvar(veiculo)
