from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.pedido import StatusPedido


class PedidoItemCreate(BaseModel):
    produto_id: str
    quantidade: int = Field(ge=1)
    preco_unitario: Decimal = Field(ge=0)
    observacao: str | None = None


class PedidoCreate(BaseModel):
    numero: str | None = None
    cliente_id: str
    status: StatusPedido = StatusPedido.PENDENTE
    data_pedido: date | None = None
    data_entrega_prevista: date | None = None
    observacao: str | None = None
    itens: list[PedidoItemCreate] = []


class PedidoUpdate(BaseModel):
    numero: str | None = None
    cliente_id: str | None = None
    status: StatusPedido | None = None
    data_pedido: date | None = None
    data_entrega_prevista: date | None = None
    observacao: str | None = None
    itens: list[PedidoItemCreate] | None = None


class PedidoItemResponse(BaseModel):
    id: str
    produto_id: str
    quantidade: int
    preco_unitario: Decimal
    observacao: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PedidoResponse(BaseModel):
    id: str
    numero: str | None
    cliente_id: str
    status: StatusPedido
    data_pedido: date | None
    data_entrega_prevista: date | None
    observacao: str | None
    itens: list[PedidoItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
