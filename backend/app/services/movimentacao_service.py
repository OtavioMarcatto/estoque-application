from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessError, NotFoundError
from app.models.movimentacao import Movimentacao, TipoMovimentacao
from app.repositories import movimentacao_repository, produto_repository
from app.schemas.movimentacao import MovimentacaoCreate


async def listar(
    db: AsyncSession,
    produto_id: str | None = None,
    tipo: TipoMovimentacao | None = None,
) -> list[Movimentacao]:
    return await movimentacao_repository.get_all(db, produto_id=produto_id, tipo=tipo)


async def registrar(db: AsyncSession, data: MovimentacaoCreate) -> Movimentacao:
    produto = await produto_repository.get_by_id(db, data.produto_id)
    if not produto:
        raise NotFoundError("Produto não encontrado")

    if data.tipo == TipoMovimentacao.SAIDA:
        if produto.quantidade < data.quantidade:
            raise BusinessError(
                f"Estoque insuficiente. Disponível: {produto.quantidade}, "
                f"solicitado: {data.quantidade}"
            )
        produto.quantidade -= data.quantidade
    else:
        produto.quantidade += data.quantidade

    await db.flush()
    movimentacao = await movimentacao_repository.create(db, data)
    return movimentacao
