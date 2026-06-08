from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey

if TYPE_CHECKING:
    from app.models.categoria import Categoria
    from app.models.fornecedor import Fornecedor
    from app.models.movimentacao import Movimentacao


class Produto(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "produtos"

    codigo: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    preco_compra: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    preco_venda: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quantidade_minima: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    categoria_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True
    )
    fornecedor_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("fornecedores.id", ondelete="SET NULL"), nullable=True
    )

    categoria: Mapped[Categoria | None] = relationship(
        "Categoria", back_populates="produtos"
    )
    fornecedor: Mapped[Fornecedor | None] = relationship(
        "Fornecedor", back_populates="produtos"
    )
    movimentacoes: Mapped[list[Movimentacao]] = relationship(
        "Movimentacao", back_populates="produto", cascade="all, delete-orphan"
    )

    @property
    def estoque_baixo(self) -> bool:
        return self.quantidade <= self.quantidade_minima and self.quantidade_minima > 0
