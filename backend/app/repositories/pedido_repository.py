from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.pedido import Pedido, PedidoItem
from app.schemas.pedido import PedidoCreate, PedidoItemCreate, PedidoUpdate


def _with_relations() -> list:
    return [
        selectinload(Pedido.cliente),
        selectinload(Pedido.itens).selectinload(PedidoItem.produto),
    ]


async def get_all(
    db: AsyncSession,
    cliente_id: str | None = None,
    status: str | None = None,
) -> list[Pedido]:
    stmt = select(Pedido).options(*_with_relations()).order_by(Pedido.created_at.desc())
    if cliente_id:
        stmt = stmt.where(Pedido.cliente_id == cliente_id)
    if status:
        stmt = stmt.where(Pedido.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, pedido_id: str) -> Pedido | None:
    result = await db.execute(
        select(Pedido).options(*_with_relations()).where(Pedido.id == pedido_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: PedidoCreate) -> Pedido:
    pedido = Pedido(
        numero=data.numero,
        cliente_id=data.cliente_id,
        status=data.status,
        data_pedido=data.data_pedido,
        data_entrega_prevista=data.data_entrega_prevista,
        observacao=data.observacao,
    )
    db.add(pedido)
    await db.flush()
    _add_itens(pedido, data.itens)
    await db.commit()
    return await get_by_id(db, pedido.id)  # type: ignore[return-value]


async def update(db: AsyncSession, pedido: Pedido, data: PedidoUpdate) -> Pedido:
    for field in (
        "numero",
        "cliente_id",
        "status",
        "data_pedido",
        "data_entrega_prevista",
        "observacao",
    ):
        value = getattr(data, field)
        if value is not None:
            setattr(pedido, field, value)
    if data.itens is not None:
        for item in list(pedido.itens):
            await db.delete(item)
        await db.flush()
        _add_itens(pedido, data.itens)
    await db.commit()
    return await get_by_id(db, pedido.id)  # type: ignore[return-value]


async def delete(db: AsyncSession, pedido: Pedido) -> None:
    await db.delete(pedido)
    await db.commit()


def _add_itens(pedido: Pedido, itens: list[PedidoItemCreate]) -> None:
    for item in itens:
        pedido.itens.append(
            PedidoItem(
                pedido_id=pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                observacao=item.observacao,
            )
        )
