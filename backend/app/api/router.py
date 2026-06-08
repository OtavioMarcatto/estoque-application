from fastapi import APIRouter

from app.api.v1 import categorias, fornecedores, movimentacoes, produtos, relatorios

router = APIRouter()

router.include_router(produtos.router, prefix="/produtos", tags=["produtos"])
router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
router.include_router(
    fornecedores.router, prefix="/fornecedores", tags=["fornecedores"]
)
router.include_router(
    movimentacoes.router, prefix="/movimentacoes", tags=["movimentacoes"]
)
router.include_router(relatorios.router, prefix="/relatorios", tags=["relatorios"])
