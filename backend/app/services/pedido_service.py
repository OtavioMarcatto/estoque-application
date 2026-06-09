from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.pedido import Pedido
from app.repositories import pedido_repository
from app.schemas.pedido import PedidoCreate, PedidoUpdate


async def listar(
    db: AsyncSession,
    cliente_id: str | None = None,
    status: str | None = None,
) -> list[Pedido]:
    return await pedido_repository.get_all(db, cliente_id=cliente_id, status=status)


async def buscar(db: AsyncSession, pedido_id: str) -> Pedido:
    pedido = await pedido_repository.get_by_id(db, pedido_id)
    if not pedido:
        raise NotFoundError("Pedido não encontrado")
    return pedido


async def criar(db: AsyncSession, data: PedidoCreate) -> Pedido:
    return await pedido_repository.create(db, data)


async def atualizar(db: AsyncSession, pedido_id: str, data: PedidoUpdate) -> Pedido:
    pedido = await buscar(db, pedido_id)
    return await pedido_repository.update(db, pedido, data)


async def deletar(db: AsyncSession, pedido_id: str) -> None:
    pedido = await buscar(db, pedido_id)
    await pedido_repository.delete(db, pedido)
