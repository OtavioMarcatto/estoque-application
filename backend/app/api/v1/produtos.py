from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessError, ConflictError
from app.dependencies import get_db
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.services import categoria_service, fornecedor_service, produto_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listar_produtos(
    request: Request,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    produtos = await produto_service.listar(db, search=search)
    return templates.TemplateResponse(
        request,
        "produtos/index.html",
        {"produtos": produtos, "search": search or ""},
    )


@router.get("/novo", response_class=HTMLResponse)
async def form_novo_produto(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    categorias = await categoria_service.listar(db)
    fornecedores = await fornecedor_service.listar(db)
    return templates.TemplateResponse(
        request,
        "produtos/form.html",
        {
            "produto": None,
            "categorias": categorias,
            "fornecedores": fornecedores,
            "errors": [],
            "form_data": {},
        },
    )


@router.post("/novo", response_model=None)
async def criar_produto(
    request: Request,
    codigo: str = Form(...),
    nome: str = Form(...),
    descricao: str = Form(""),
    preco_compra: str = Form("0"),
    preco_venda: str = Form("0"),
    quantidade: int = Form(0),
    quantidade_minima: int = Form(0),
    categoria_id: str = Form(""),
    fornecedor_id: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        data = ProdutoCreate(
            codigo=codigo,
            nome=nome,
            descricao=descricao or None,
            preco_compra=preco_compra,  # type: ignore[arg-type]
            preco_venda=preco_venda,  # type: ignore[arg-type]
            quantidade=quantidade,
            quantidade_minima=quantidade_minima,
            categoria_id=categoria_id or None,
            fornecedor_id=fornecedor_id or None,
        )
        await produto_service.criar(db, data)
        return RedirectResponse(url="/produtos", status_code=303)
    except (ConflictError, BusinessError) as e:
        categorias = await categoria_service.listar(db)
        fornecedores = await fornecedor_service.listar(db)
        form_data = await request.form()
        return templates.TemplateResponse(
            request,
            "produtos/form.html",
            {
                "produto": None,
                "categorias": categorias,
                "fornecedores": fornecedores,
                "errors": [e.detail],
                "form_data": form_data,
            },
            status_code=422,
        )


@router.get("/{produto_id}", response_class=HTMLResponse)
async def detalhar_produto(
    request: Request,
    produto_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    produto = await produto_service.buscar(db, produto_id)
    categorias = await categoria_service.listar(db)
    fornecedores = await fornecedor_service.listar(db)
    return templates.TemplateResponse(
        request,
        "produtos/form.html",
        {
            "produto": produto,
            "categorias": categorias,
            "fornecedores": fornecedores,
            "errors": [],
            "form_data": {},
        },
    )


@router.post("/{produto_id}", response_model=None)
async def atualizar_produto(
    request: Request,
    produto_id: str,
    codigo: str = Form(...),
    nome: str = Form(...),
    descricao: str = Form(""),
    preco_compra: str = Form("0"),
    preco_venda: str = Form("0"),
    quantidade_minima: int = Form(0),
    categoria_id: str = Form(""),
    fornecedor_id: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        data = ProdutoUpdate(
            codigo=codigo,
            nome=nome,
            descricao=descricao or None,
            preco_compra=preco_compra,  # type: ignore[arg-type]
            preco_venda=preco_venda,  # type: ignore[arg-type]
            quantidade_minima=quantidade_minima,
            categoria_id=categoria_id or None,
            fornecedor_id=fornecedor_id or None,
        )
        await produto_service.atualizar(db, produto_id, data)
        return RedirectResponse(url="/produtos", status_code=303)
    except (ConflictError, BusinessError) as e:
        produto = await produto_service.buscar(db, produto_id)
        categorias = await categoria_service.listar(db)
        fornecedores = await fornecedor_service.listar(db)
        return templates.TemplateResponse(
            request,
            "produtos/form.html",
            {
                "produto": produto,
                "categorias": categorias,
                "fornecedores": fornecedores,
                "errors": [e.detail],
            },
            status_code=422,
        )


@router.delete("/{produto_id}")
async def deletar_produto(
    produto_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    await produto_service.deletar(db, produto_id)
    return HTMLResponse(content="", status_code=200)
