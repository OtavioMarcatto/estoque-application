from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


async def get_all(db: AsyncSession) -> list[Categoria]:
    result = await db.execute(select(Categoria).order_by(Categoria.nome))
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, categoria_id: str) -> Categoria | None:
    result = await db.execute(select(Categoria).where(Categoria.id == categoria_id))
    return result.scalar_one_or_none()


async def get_by_nome(db: AsyncSession, nome: str) -> Categoria | None:
    result = await db.execute(select(Categoria).where(Categoria.nome == nome))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: CategoriaCreate) -> Categoria:
    categoria = Categoria(**data.model_dump())
    db.add(categoria)
    await db.commit()
    await db.refresh(categoria)
    return categoria


async def update(db: AsyncSession, categoria: Categoria, data: CategoriaUpdate) -> Categoria:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(categoria, field, value)
    await db.commit()
    await db.refresh(categoria)
    return categoria


async def delete(db: AsyncSession, categoria: Categoria) -> None:
    await db.delete(categoria)
    await db.commit()
