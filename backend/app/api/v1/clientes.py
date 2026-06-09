from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.dependencies import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.services import cliente_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listar_clientes(
    request: Request,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    clientes = await cliente_service.listar(db, search=search)
    return templates.TemplateResponse(
        request,
        "clientes/index.html",
        {"clientes": clientes, "search": search or ""},
    )


@router.get("/novo", response_class=HTMLResponse)
async def form_novo_cliente(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "clientes/form.html",
        {"cliente": None, "errors": [], "form_data": {}},
    )


@router.post("/novo", response_model=None)
async def criar_cliente(
    request: Request,
    nome: str = Form(...),
    codigo: str = Form(""),
    contrato: str = Form(""),
    data_do_pedido: str = Form(""),
    data_da_entrega: str = Form(""),
    descricao_do_pedido: str = Form(""),
    cnpj: str = Form(""),
    cpf: str = Form(""),
    ie: str = Form(""),
    rg: str = Form(""),
    endereco: str = Form(""),
    bairro: str = Form(""),
    cidade: str = Form(""),
    estado: str = Form(""),
    cep: str = Form(""),
    celular: str = Form(""),
    email: str = Form(""),
    responsavel_legal: str = Form(""),
    cpf_responsavel_legal: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        from datetime import date

        def to_date(s: str) -> date | None:
            s = s.strip()
            if not s:
                return None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    from datetime import datetime

                    return datetime.strptime(s, fmt).date()
                except ValueError:
                    continue
            return None

        data = ClienteCreate(
            nome=nome,
            codigo=codigo or None,
            contrato=contrato or None,
            data_do_pedido=to_date(data_do_pedido),
            data_da_entrega=to_date(data_da_entrega),
            descricao_do_pedido=descricao_do_pedido or None,
            cnpj=cnpj or None,
            cpf=cpf or None,
            ie=ie or None,
            rg=rg or None,
            endereco=endereco or None,
            bairro=bairro or None,
            cidade=cidade or None,
            estado=estado or None,
            cep=cep or None,
            celular=celular or None,
            email=email or None,
            responsavel_legal=responsavel_legal or None,
            cpf_responsavel_legal=cpf_responsavel_legal or None,
        )
        await cliente_service.criar(db, data)
        return RedirectResponse(url="/clientes", status_code=303)
    except Exception as e:
        form_data = await request.form()
        return templates.TemplateResponse(
            request,
            "clientes/form.html",
            {"cliente": None, "errors": [str(e)], "form_data": form_data},
            status_code=422,
        )


@router.get("/importar", response_class=HTMLResponse)
async def form_importar(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "clientes/upload.html", {"result": None})


@router.post("/importar", response_model=None)
async def importar_xlsx(
    request: Request,
    arquivo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    conteudo = await arquivo.read()
    result = await cliente_service.importar_xlsx(db, conteudo)
    return templates.TemplateResponse(
        request, "clientes/upload.html", {"result": result}
    )


@router.get("/{cliente_id}", response_class=HTMLResponse)
async def detalhar_cliente(
    request: Request,
    cliente_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    cliente = await cliente_service.buscar(db, cliente_id)
    return templates.TemplateResponse(
        request,
        "clientes/form.html",
        {"cliente": cliente, "errors": [], "form_data": {}},
    )


@router.post("/{cliente_id}", response_model=None)
async def atualizar_cliente(
    request: Request,
    cliente_id: str,
    nome: str = Form(...),
    codigo: str = Form(""),
    contrato: str = Form(""),
    data_do_pedido: str = Form(""),
    data_da_entrega: str = Form(""),
    descricao_do_pedido: str = Form(""),
    cnpj: str = Form(""),
    cpf: str = Form(""),
    ie: str = Form(""),
    rg: str = Form(""),
    endereco: str = Form(""),
    bairro: str = Form(""),
    cidade: str = Form(""),
    estado: str = Form(""),
    cep: str = Form(""),
    celular: str = Form(""),
    email: str = Form(""),
    responsavel_legal: str = Form(""),
    cpf_responsavel_legal: str = Form(""),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        from datetime import date, datetime

        def to_date(s: str) -> date | None:
            s = s.strip()
            if not s:
                return None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    return datetime.strptime(s, fmt).date()
                except ValueError:
                    continue
            return None

        data = ClienteUpdate(
            nome=nome,
            codigo=codigo or None,
            contrato=contrato or None,
            data_do_pedido=to_date(data_do_pedido),
            data_da_entrega=to_date(data_da_entrega),
            descricao_do_pedido=descricao_do_pedido or None,
            cnpj=cnpj or None,
            cpf=cpf or None,
            ie=ie or None,
            rg=rg or None,
            endereco=endereco or None,
            bairro=bairro or None,
            cidade=cidade or None,
            estado=estado or None,
            cep=cep or None,
            celular=celular or None,
            email=email or None,
            responsavel_legal=responsavel_legal or None,
            cpf_responsavel_legal=cpf_responsavel_legal or None,
        )
        await cliente_service.atualizar(db, cliente_id, data)
        return RedirectResponse(url="/clientes", status_code=303)
    except NotFoundError:
        raise
    except Exception as e:
        cliente = await cliente_service.buscar(db, cliente_id)
        return templates.TemplateResponse(
            request,
            "clientes/form.html",
            {"cliente": cliente, "errors": [str(e)], "form_data": {}},
            status_code=422,
        )


@router.delete("/{cliente_id}")
async def deletar_cliente(
    cliente_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    await cliente_service.deletar(db, cliente_id)
    return HTMLResponse(content="", status_code=200)
