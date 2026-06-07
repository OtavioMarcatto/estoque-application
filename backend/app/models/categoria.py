from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey

if TYPE_CHECKING:
    from app.models.produto import Produto


class Categoria(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "categorias"

    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    produtos: Mapped[list[Produto]] = relationship("Produto", back_populates="categoria")
