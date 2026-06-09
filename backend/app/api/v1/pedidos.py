from datetime import date, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.dependencies import get_db
from app.models.pedido import StatusPedido
from app.schemas.pedido import PedidoCreate, PedidoItemCreate, PedidoUpdate
from app.services import cliente_service, pedido_service, produto_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

STATUS_LABELS = {
    StatusPedido.PENDENTE: "Pendente",
    StatusPedido.EM_ANDAMENTO: "Em andamento",
    StatusPedido.CONCLUIDO: "Concluído",
    StatusPedido.CANCELADO: "Cancelado",
}


def _to_date(s: str) -> date | None:
    s = s.strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _parse_itens(
    produto_ids: list[str],
    quantidades: list[str],
    precos: list[str],
    observacoes: list[str],
) -> list[PedidoItemCreate]:
    itens = []
    for pid, qty, preco, obs in zip(produto_ids, quantidades, precos, observacoes, strict=False):
        if not pid.strip():
            continue
        itens.append(
            PedidoItemCreate(
                produto_id=pid.strip(),
                quantidade=int(qty) if qty.strip() else 1,
                preco_unitario=Decimal(preco.replace(",", ".")) if preco.strip() else Decimal("0"),
                observacao=obs.strip() or None,
            )
        )
    return itens


@router.get("/", response_class=HTMLResponse)
async def listar_pedidos(
    request: Request,
    cliente_id: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    pedidos = await pedido_service.listar(db, cliente_id=cliente_id, status=status)
    clientes = await cliente_service.listar(db)
    return templates.TemplateResponse(
        request,
        "pedidos/index.html",
        {
            "pedidos": pedidos,
            "clientes": clientes,
            "filtro_cliente_id": cliente_id or "",
            "filtro_status": status or "",
            "status_labels": STATUS_LABELS,
            "status_opcoes": list(StatusPedido),
        },
    )


@router.get("/novo", response_class=HTMLResponse)
async def form_novo_pedido(
    request: Request,
    cliente_id: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    clientes = await cliente_service.listar(db)
    produtos = await produto_service.listar(db)
    return templates.TemplateResponse(
        request,
        "pedidos/form.html",
        {
            "pedido": None,
            "clientes": clientes,
            "produtos": produtos,
            "cliente_id_selecionado": cliente_id or "",
            "status_opcoes": list(StatusPedido),
            "status_labels": STATUS_LABELS,
            "errors": [],
        },
    )


@router.post("/novo", response_model=None)
async def criar_pedido(
    request: Request,
    cliente_id: str = Form(...),
    numero: str = Form(""),
    status: str = Form("pendente"),
    data_pedido: str = Form(""),
    data_entrega_prevista: str = Form(""),
    observacao: str = Form(""),
    produto_ids: list[str] = Form(default=[]),
    quantidades: list[str] = Form(default=[]),
    precos: list[str] = Form(default=[]),
    obs_itens: list[str] = Form(default=[]),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        itens = _parse_itens(produto_ids, quantidades, precos, obs_itens)
        data = PedidoCreate(
            numero=numero or None,
            cliente_id=cliente_id,
            status=StatusPedido(status),
            data_pedido=_to_date(data_pedido),
            data_entrega_prevista=_to_date(data_entrega_prevista),
            observacao=observacao or None,
            itens=itens,
        )
        pedido = await pedido_service.criar(db, data)
        return RedirectResponse(url=f"/pedidos/{pedido.id}", status_code=303)
    except Exception as e:
        clientes = await cliente_service.listar(db)
        produtos = await produto_service.listar(db)
        return templates.TemplateResponse(
            request,
            "pedidos/form.html",
            {
                "pedido": None,
                "clientes": clientes,
                "produtos": produtos,
                "cliente_id_selecionado": cliente_id,
                "status_opcoes": list(StatusPedido),
                "status_labels": STATUS_LABELS,
                "errors": [str(e)],
            },
            status_code=422,
        )


@router.get("/{pedido_id}", response_class=HTMLResponse)
async def detalhar_pedido(
    request: Request,
    pedido_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    pedido = await pedido_service.buscar(db, pedido_id)
    clientes = await cliente_service.listar(db)
    produtos = await produto_service.listar(db)
    return templates.TemplateResponse(
        request,
        "pedidos/form.html",
        {
            "pedido": pedido,
            "clientes": clientes,
            "produtos": produtos,
            "cliente_id_selecionado": pedido.cliente_id,
            "status_opcoes": list(StatusPedido),
            "status_labels": STATUS_LABELS,
            "errors": [],
        },
    )


@router.post("/{pedido_id}", response_model=None)
async def atualizar_pedido(
    request: Request,
    pedido_id: str,
    cliente_id: str = Form(...),
    numero: str = Form(""),
    status: str = Form("pendente"),
    data_pedido: str = Form(""),
    data_entrega_prevista: str = Form(""),
    observacao: str = Form(""),
    produto_ids: list[str] = Form(default=[]),
    quantidades: list[str] = Form(default=[]),
    precos: list[str] = Form(default=[]),
    obs_itens: list[str] = Form(default=[]),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse | HTMLResponse:
    try:
        itens = _parse_itens(produto_ids, quantidades, precos, obs_itens)
        data = PedidoUpdate(
            numero=numero or None,
            cliente_id=cliente_id,
            status=StatusPedido(status),
            data_pedido=_to_date(data_pedido),
            data_entrega_prevista=_to_date(data_entrega_prevista),
            observacao=observacao or None,
            itens=itens,
        )
        await pedido_service.atualizar(db, pedido_id, data)
        return RedirectResponse(url=f"/pedidos/{pedido_id}", status_code=303)
    except NotFoundError:
        raise
    except Exception as e:
        pedido = await pedido_service.buscar(db, pedido_id)
        clientes = await cliente_service.listar(db)
        produtos = await produto_service.listar(db)
        return templates.TemplateResponse(
            request,
            "pedidos/form.html",
            {
                "pedido": pedido,
                "clientes": clientes,
                "produtos": produtos,
                "cliente_id_selecionado": cliente_id,
                "status_opcoes": list(StatusPedido),
                "status_labels": STATUS_LABELS,
                "errors": [str(e)],
            },
            status_code=422,
        )


@router.delete("/{pedido_id}")
async def deletar_pedido(
    pedido_id: str,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    await pedido_service.deletar(db, pedido_id)
    return HTMLResponse(content="", status_code=200)
