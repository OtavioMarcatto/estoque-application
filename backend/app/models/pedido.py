from __future__ import annotations

import enum
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.produto import Produto


class StatusPedido(enum.StrEnum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class Pedido(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "pedidos"

    numero: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    cliente_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status: Mapped[StatusPedido] = mapped_column(
        Enum(StatusPedido), nullable=False, default=StatusPedido.PENDENTE
    )
    data_pedido: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_entrega_prevista: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)

    cliente: Mapped[Cliente] = relationship("Cliente")
    itens: Mapped[list[PedidoItem]] = relationship(
        "PedidoItem", back_populates="pedido", cascade="all, delete-orphan"
    )

    @property
    def total(self) -> Decimal:
        return sum(
            (item.quantidade * item.preco_unitario for item in self.itens),
            Decimal("0"),
        )


class PedidoItem(Base, UUIDPrimaryKey):
    __tablename__ = "pedido_itens"

    pedido_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    produto_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    observacao: Mapped[str | None] = mapped_column(String(300), nullable=True)

    pedido: Mapped[Pedido] = relationship("Pedido", back_populates="itens")
    produto: Mapped[Produto] = relationship("Produto")
