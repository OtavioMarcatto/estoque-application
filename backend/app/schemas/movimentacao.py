from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.movimentacao import TipoMovimentacao


class MovimentacaoCreate(BaseModel):
    produto_id: str
    tipo: TipoMovimentacao
    quantidade: int = Field(gt=0)
    motivo: str | None = None
    observacao: str | None = None


class MovimentacaoResponse(BaseModel):
    id: str
    produto_id: str
    tipo: TipoMovimentacao
    quantidade: int
    motivo: str | None
    observacao: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
