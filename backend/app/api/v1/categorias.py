from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.dependencies import get_db
from app.schemas.categoria import CategoriaCreate
from app.services import categoria_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listar_categorias(request: Request, db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    categorias = await categoria_service.listar(db)
    return templates.TemplateResponse(
        request,
        "produtos/categorias.html",
        {"categorias": categorias},
    )


@router.post("/", response_model=None)
async def criar_categoria(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        data = CategoriaCreate(nome=nome, descricao=descricao or None)
        await categoria_service.criar(db, data)
        return RedirectResponse(url="/categorias", status_code=303)
    except ConflictError as e:
        categorias = await categoria_service.listar(db)
        return templates.TemplateResponse(
            request,
            "produtos/categorias.html",
            {"categorias": categorias, "errors": [e.detail]},
            status_code=422,
        )


@router.delete("/{categoria_id}")
async def deletar_categoria(
    categoria_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    await categoria_service.deletar(db, categoria_id)
    return HTMLResponse(content="", status_code=200)
