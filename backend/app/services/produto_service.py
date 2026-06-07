from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.produto import Produto
from app.repositories import produto_repository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


async def listar(db: AsyncSession, search: str | None = None) -> list[Produto]:
    return await produto_repository.get_all(db, search=search)


async def buscar(db: AsyncSession, produto_id: str) -> Produto:
    produto = await produto_repository.get_by_id(db, produto_id)
    if not produto:
        raise NotFoundError("Produto não encontrado")
    return produto


async def criar(db: AsyncSession, data: ProdutoCreate) -> Produto:
    existente = await produto_repository.get_by_codigo(db, data.codigo)
    if existente:
        raise ConflictError(f"Código '{data.codigo}' já cadastrado")
    return await produto_repository.create(db, data)


async def atualizar(db: AsyncSession, produto_id: str, data: ProdutoUpdate) -> Produto:
    produto = await buscar(db, produto_id)
    if data.codigo:
        existente = await produto_repository.get_by_codigo(db, data.codigo)
        if existente and existente.id != produto_id:
            raise ConflictError(f"Código '{data.codigo}' já cadastrado")
    return await produto_repository.update(db, produto, data)


async def deletar(db: AsyncSession, produto_id: str) -> None:
    produto = await buscar(db, produto_id)
    await produto_repository.delete(db, produto)
