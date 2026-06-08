from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.fornecedor import Fornecedor
from app.repositories import fornecedor_repository
from app.schemas.fornecedor import FornecedorCreate, FornecedorUpdate


async def listar(db: AsyncSession) -> list[Fornecedor]:
    return await fornecedor_repository.get_all(db)


async def buscar(db: AsyncSession, fornecedor_id: str) -> Fornecedor:
    fornecedor = await fornecedor_repository.get_by_id(db, fornecedor_id)
    if not fornecedor:
        raise NotFoundError("Fornecedor não encontrado")
    return fornecedor


async def criar(db: AsyncSession, data: FornecedorCreate) -> Fornecedor:
    if data.cnpj:
        existente = await fornecedor_repository.get_by_cnpj(db, data.cnpj)
        if existente:
            raise ConflictError(f"CNPJ '{data.cnpj}' já cadastrado")
    return await fornecedor_repository.create(db, data)


async def atualizar(
    db: AsyncSession, fornecedor_id: str, data: FornecedorUpdate
) -> Fornecedor:
    fornecedor = await buscar(db, fornecedor_id)
    if data.cnpj:
        existente = await fornecedor_repository.get_by_cnpj(db, data.cnpj)
        if existente and existente.id != fornecedor_id:
            raise ConflictError(f"CNPJ '{data.cnpj}' já cadastrado")
    return await fornecedor_repository.update(db, fornecedor, data)


async def deletar(db: AsyncSession, fornecedor_id: str) -> None:
    fornecedor = await buscar(db, fornecedor_id)
    await fornecedor_repository.delete(db, fornecedor)
