from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fornecedor import Fornecedor
from app.schemas.fornecedor import FornecedorCreate, FornecedorUpdate


async def get_all(db: AsyncSession) -> list[Fornecedor]:
    result = await db.execute(select(Fornecedor).order_by(Fornecedor.nome))
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, fornecedor_id: str) -> Fornecedor | None:
    result = await db.execute(select(Fornecedor).where(Fornecedor.id == fornecedor_id))
    return result.scalar_one_or_none()


async def get_by_cnpj(db: AsyncSession, cnpj: str) -> Fornecedor | None:
    result = await db.execute(select(Fornecedor).where(Fornecedor.cnpj == cnpj))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: FornecedorCreate) -> Fornecedor:
    fornecedor = Fornecedor(**data.model_dump())
    db.add(fornecedor)
    await db.commit()
    await db.refresh(fornecedor)
    return fornecedor


async def update(
    db: AsyncSession, fornecedor: Fornecedor, data: FornecedorUpdate
) -> Fornecedor:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(fornecedor, field, value)
    await db.commit()
    await db.refresh(fornecedor)
    return fornecedor


async def delete(db: AsyncSession, fornecedor: Fornecedor) -> None:
    await db.delete(fornecedor)
    await db.commit()
