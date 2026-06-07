from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey

if TYPE_CHECKING:
    from app.models.produto import Produto


class TipoMovimentacao(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class Movimentacao(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "movimentacoes"

    produto_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tipo: Mapped[TipoMovimentacao] = mapped_column(
        Enum(TipoMovimentacao), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(200), nullable=True)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)

    produto: Mapped[Produto] = relationship("Produto", back_populates="movimentacoes")
