from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


async def get_all(db: AsyncSession, search: str | None = None) -> list[Cliente]:
    stmt = select(Cliente).order_by(Cliente.nome)
    if search:
        term = f"%{search}%"
        stmt = stmt.where(
            or_(
                Cliente.nome.ilike(term),
                Cliente.codigo.ilike(term),
                Cliente.cnpj.ilike(term),
                Cliente.cpf.ilike(term),
            )
        )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, cliente_id: str) -> Cliente | None:
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: ClienteCreate) -> Cliente:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def create_many(db: AsyncSession, items: list[ClienteCreate]) -> list[Cliente]:
    clientes = [Cliente(**item.model_dump()) for item in items]
    db.add_all(clientes)
    await db.commit()
    return clientes


async def update(db: AsyncSession, cliente: Cliente, data: ClienteUpdate) -> Cliente:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, field, value)
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def delete(db: AsyncSession, cliente: Cliente) -> None:
    await db.delete(cliente)
    await db.commit()
