from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def _with_relations() -> list:
    return [selectinload(Produto.categoria), selectinload(Produto.fornecedor)]


async def get_all(db: AsyncSession, search: str | None = None) -> list[Produto]:
    stmt = select(Produto).options(*_with_relations()).order_by(Produto.nome)
    if search:
        term = f"%{search}%"
        stmt = stmt.where(Produto.nome.ilike(term) | Produto.codigo.ilike(term))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, produto_id: str) -> Produto | None:
    result = await db.execute(
        select(Produto).options(*_with_relations()).where(Produto.id == produto_id)
    )
    return result.scalar_one_or_none()


async def get_by_codigo(db: AsyncSession, codigo: str) -> Produto | None:
    result = await db.execute(select(Produto).where(Produto.codigo == codigo))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: ProdutoCreate) -> Produto:
    produto = Produto(**data.model_dump())
    db.add(produto)
    await db.commit()
    await db.refresh(produto)
    return await get_by_id(db, produto.id)  # type: ignore[return-value]


async def update(db: AsyncSession, produto: Produto, data: ProdutoUpdate) -> Produto:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(produto, field, value)
    await db.commit()
    return await get_by_id(db, produto.id)  # type: ignore[return-value]


async def delete(db: AsyncSession, produto: Produto) -> None:
    await db.delete(produto)
    await db.commit()
