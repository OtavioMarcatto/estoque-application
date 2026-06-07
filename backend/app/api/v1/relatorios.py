from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.services import movimentacao_service, produto_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/estoque", response_class=HTMLResponse)
async def relatorio_estoque(
    request: Request, db: AsyncSession = Depends(get_db)
) -> HTMLResponse:
    produtos = await produto_service.listar(db)
    produtos_baixo = [p for p in produtos if p.estoque_baixo]
    return templates.TemplateResponse(
        request,
        "relatorios/estoque.html",
        {
            "produtos": produtos,
            "produtos_baixo_estoque": produtos_baixo,
            "total_produtos": len(produtos),
            "total_baixo_estoque": len(produtos_baixo),
        },
    )


@router.get("/movimentacoes", response_class=HTMLResponse)
async def relatorio_movimentacoes(
    request: Request,
    produto_id: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    movimentacoes = await movimentacao_service.listar(db, produto_id=produto_id)
    produtos = await produto_service.listar(db)
    return templates.TemplateResponse(
        request,
        "relatorios/movimentacoes.html",
        {
            "movimentacoes": movimentacoes,
            "produtos": produtos,
            "filtro_produto_id": produto_id or "",
        },
    )
