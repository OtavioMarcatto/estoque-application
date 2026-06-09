from fastapi import APIRouter

from app.api.v1 import (
    categorias,
    clientes,
    fornecedores,
    movimentacoes,
    pedidos,
    produtos,
    relatorios,
)

router = APIRouter()

router.include_router(produtos.router, prefix="/produtos", tags=["produtos"])
router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
router.include_router(pedidos.router, prefix="/pedidos", tags=["pedidos"])
router.include_router(
    fornecedores.router, prefix="/fornecedores", tags=["fornecedores"]
)
router.include_router(
    movimentacoes.router, prefix="/movimentacoes", tags=["movimentacoes"]
)
router.include_router(relatorios.router, prefix="/relatorios", tags=["relatorios"])
