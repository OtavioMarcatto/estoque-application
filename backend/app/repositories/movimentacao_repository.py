from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.movimentacao import Movimentacao, TipoMovimentacao
from app.schemas.movimentacao import MovimentacaoCreate


async def get_all(
    db: AsyncSession,
    produto_id: str | None = None,
    tipo: TipoMovimentacao | None = None,
    limit: int = 100,
) -> list[Movimentacao]:
    stmt = (
        select(Movimentacao)
        .options(selectinload(Movimentacao.produto))
        .order_by(Movimentacao.created_at.desc())
        .limit(limit)
    )
    if produto_id:
        stmt = stmt.where(Movimentacao.produto_id == produto_id)
    if tipo:
        stmt = stmt.where(Movimentacao.tipo == tipo)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, movimentacao_id: str) -> Movimentacao | None:
    result = await db.execute(
        select(Movimentacao)
        .options(selectinload(Movimentacao.produto))
        .where(Movimentacao.id == movimentacao_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: MovimentacaoCreate) -> Movimentacao:
    movimentacao = Movimentacao(**data.model_dump())
    db.add(movimentacao)
    await db.commit()
    await db.refresh(movimentacao)
    return await get_by_id(db, movimentacao.id)  # type: ignore[return-value]
