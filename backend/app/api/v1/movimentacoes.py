from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessError, NotFoundError
from app.dependencies import get_db
from app.models.movimentacao import TipoMovimentacao
from app.schemas.movimentacao import MovimentacaoCreate
from app.services import movimentacao_service, produto_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listar_movimentacoes(
    request: Request,
    produto_id: str | None = None,
    tipo: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    tipo_enum = TipoMovimentacao(tipo) if tipo in ("ENTRADA", "SAIDA") else None
    movimentacoes = await movimentacao_service.listar(
        db, produto_id=produto_id, tipo=tipo_enum
    )
    produtos = await produto_service.listar(db)
    return templates.TemplateResponse(
        request,
        "movimentacoes/index.html",
        {
            "movimentacoes": movimentacoes,
            "produtos": produtos,
            "filtro_produto_id": produto_id or "",
            "filtro_tipo": tipo or "",
        },
    )


@router.get("/nova", response_class=HTMLResponse)
async def form_nova_movimentacao(
    request: Request,
    produto_id: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    produtos = await produto_service.listar(db)
    return templates.TemplateResponse(
        request,
        "movimentacoes/form.html",
        {
            "produtos": produtos,
            "produto_id_selecionado": produto_id or "",
            "errors": [],
        },
    )


@router.post("/nova", response_model=None)
async def registrar_movimentacao(
    request: Request,
    produto_id: str = Form(...),
    tipo: str = Form(...),
    quantidade: int = Form(...),
    motivo: str = Form(""),
    observacao: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        data = MovimentacaoCreate(
            produto_id=produto_id,
            tipo=TipoMovimentacao(tipo),
            quantidade=quantidade,
            motivo=motivo or None,
            observacao=observacao or None,
        )
        await movimentacao_service.registrar(db, data)
        return RedirectResponse(url="/movimentacoes", status_code=303)
    except (BusinessError, NotFoundError) as e:
        produtos = await produto_service.listar(db)
        return templates.TemplateResponse(
            request,
            "movimentacoes/form.html",
            {
                "produtos": produtos,
                "produto_id_selecionado": produto_id,
                "errors": [e.detail],
            },
            status_code=422,
        )
