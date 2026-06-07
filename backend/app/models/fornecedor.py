from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey

if TYPE_CHECKING:
    from app.models.produto import Produto


class Fornecedor(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "fornecedores"

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cnpj: Mapped[str | None] = mapped_column(String(18), nullable=True, unique=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(300), nullable=True)

    produtos: Mapped[list[Produto]] = relationship("Produto", back_populates="fornecedor")
