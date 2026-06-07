from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.dependencies import get_db
from app.schemas.fornecedor import FornecedorCreate, FornecedorUpdate
from app.services import fornecedor_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listar_fornecedores(
    request: Request, db: AsyncSession = Depends(get_db)
) -> HTMLResponse:
    fornecedores = await fornecedor_service.listar(db)
    return templates.TemplateResponse(
        request,
        "fornecedores/index.html",
        {"fornecedores": fornecedores, "errors": []},
    )


@router.get("/novo", response_class=HTMLResponse)
async def form_novo_fornecedor(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "fornecedores/form.html",
        {"fornecedor": None, "errors": []},
    )


@router.post("/novo", response_model=None)
async def criar_fornecedor(
    request: Request,
    nome: str = Form(...),
    cnpj: str = Form(""),
    telefone: str = Form(""),
    email: str = Form(""),
    endereco: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        data = FornecedorCreate(
            nome=nome,
            cnpj=cnpj or None,
            telefone=telefone or None,
            email=email or None,
            endereco=endereco or None,
        )
        await fornecedor_service.criar(db, data)
        return RedirectResponse(url="/fornecedores", status_code=303)
    except ConflictError as e:
        return templates.TemplateResponse(
            request,
            "fornecedores/form.html",
            {"fornecedor": None, "errors": [e.detail]},
            status_code=422,
        )


@router.get("/{fornecedor_id}", response_class=HTMLResponse)
async def detalhar_fornecedor(
    request: Request, fornecedor_id: str, db: AsyncSession = Depends(get_db)
) -> HTMLResponse:
    fornecedor = await fornecedor_service.buscar(db, fornecedor_id)
    return templates.TemplateResponse(
        request,
        "fornecedores/form.html",
        {"fornecedor": fornecedor, "errors": []},
    )


@router.post("/{fornecedor_id}", response_model=None)
async def atualizar_fornecedor(
    request: Request,
    fornecedor_id: str,
    nome: str = Form(...),
    cnpj: str = Form(""),
    telefone: str = Form(""),
    email: str = Form(""),
    endereco: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        data = FornecedorUpdate(
            nome=nome,
            cnpj=cnpj or None,
            telefone=telefone or None,
            email=email or None,
            endereco=endereco or None,
        )
        await fornecedor_service.atualizar(db, fornecedor_id, data)
        return RedirectResponse(url="/fornecedores", status_code=303)
    except ConflictError as e:
        fornecedor = await fornecedor_service.buscar(db, fornecedor_id)
        return templates.TemplateResponse(
            request,
            "fornecedores/form.html",
            {"fornecedor": fornecedor, "errors": [e.detail]},
            status_code=422,
        )


@router.delete("/{fornecedor_id}")
async def deletar_fornecedor(
    fornecedor_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    await fornecedor_service.deletar(db, fornecedor_id)
    return HTMLResponse(content="", status_code=200)
