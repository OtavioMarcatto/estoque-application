"""Script para popular o banco com dados de exemplo."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.core.database import AsyncSessionLocal, engine
from app.models import Base
from app.schemas.categoria import CategoriaCreate
from app.schemas.fornecedor import FornecedorCreate
from app.schemas.movimentacao import MovimentacaoCreate
from app.schemas.produto import ProdutoCreate
from app.services import categoria_service, fornecedor_service, movimentacao_service, produto_service
from app.models.movimentacao import TipoMovimentacao


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        cat_eletro = await categoria_service.criar(db, CategoriaCreate(nome="Eletrônicos"))
        cat_info = await categoria_service.criar(db, CategoriaCreate(nome="Informática"))

        forn = await fornecedor_service.criar(
            db,
            FornecedorCreate(nome="Tech Distribuidora", cnpj="12.345.678/0001-90", telefone="(11) 9999-0000"),
        )

        p1 = await produto_service.criar(
            db,
            ProdutoCreate(
                codigo="NOTE-001",
                nome="Notebook Dell Inspiron 15",
                preco_compra="3500.00",
                preco_venda="4200.00",
                quantidade=0,
                quantidade_minima=2,
                categoria_id=cat_info.id,
                fornecedor_id=forn.id,
            ),
        )
        p2 = await produto_service.criar(
            db,
            ProdutoCreate(
                codigo="MOUSE-001",
                nome="Mouse Sem Fio Logitech",
                preco_compra="80.00",
                preco_venda="129.90",
                quantidade=0,
                quantidade_minima=5,
                categoria_id=cat_info.id,
                fornecedor_id=forn.id,
            ),
        )
        p3 = await produto_service.criar(
            db,
            ProdutoCreate(
                codigo="CABO-001",
                nome="Cabo HDMI 2m",
                preco_compra="15.00",
                preco_venda="29.90",
                quantidade=0,
                quantidade_minima=10,
                categoria_id=cat_eletro.id,
            ),
        )

        for produto, qty in [(p1, 10), (p2, 30), (p3, 50)]:
            await movimentacao_service.registrar(
                db,
                MovimentacaoCreate(
                    produto_id=produto.id,
                    tipo=TipoMovimentacao.ENTRADA,
                    quantidade=qty,
                    motivo="Estoque inicial",
                ),
            )

        print("Banco populado com sucesso!")
        print(f"  Categorias: 2")
        print(f"  Fornecedores: 1")
        print(f"  Produtos: 3")
        print(f"  Movimentações: 3")


if __name__ == "__main__":
    asyncio.run(seed())
