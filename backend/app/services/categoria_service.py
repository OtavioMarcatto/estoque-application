from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.categoria import Categoria
from app.repositories import categoria_repository
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


async def listar(db: AsyncSession) -> list[Categoria]:
    return await categoria_repository.get_all(db)


async def buscar(db: AsyncSession, categoria_id: str) -> Categoria:
    categoria = await categoria_repository.get_by_id(db, categoria_id)
    if not categoria:
        raise NotFoundError("Categoria não encontrada")
    return categoria


async def criar(db: AsyncSession, data: CategoriaCreate) -> Categoria:
    existente = await categoria_repository.get_by_nome(db, data.nome)
    if existente:
        raise ConflictError(f"Categoria '{data.nome}' já existe")
    return await categoria_repository.create(db, data)


async def atualizar(db: AsyncSession, categoria_id: str, data: CategoriaUpdate) -> Categoria:
    categoria = await buscar(db, categoria_id)
    if data.nome:
        existente = await categoria_repository.get_by_nome(db, data.nome)
        if existente and existente.id != categoria_id:
            raise ConflictError(f"Categoria '{data.nome}' já existe")
    return await categoria_repository.update(db, categoria, data)


async def deletar(db: AsyncSession, categoria_id: str) -> None:
    categoria = await buscar(db, categoria_id)
    await categoria_repository.delete(db, categoria)
