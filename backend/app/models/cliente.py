from __future__ import annotations

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPrimaryKey


class Cliente(Base, UUIDPrimaryKey, TimestampMixin):
    __tablename__ = "clientes"

    codigo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    contrato: Mapped[str | None] = mapped_column(String(100), nullable=True)
    data_do_pedido: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_da_entrega: Mapped[date | None] = mapped_column(Date, nullable=True)
    descricao_do_pedido: Mapped[str | None] = mapped_column(Text, nullable=True)
    cnpj: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
    ie: Mapped[str | None] = mapped_column(String(20), nullable=True)
    rg: Mapped[str | None] = mapped_column(String(20), nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(300), nullable=True)
    bairro: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cidade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estado: Mapped[str | None] = mapped_column(String(2), nullable=True)
    cep: Mapped[str | None] = mapped_column(String(10), nullable=True)
    celular: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    responsavel_legal: Mapped[str | None] = mapped_column(String(200), nullable=True)
    cpf_responsavel_legal: Mapped[str | None] = mapped_column(String(14), nullable=True)
