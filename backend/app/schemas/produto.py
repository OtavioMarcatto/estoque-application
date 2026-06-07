from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProdutoBase(BaseModel):
    codigo: str
    nome: str
    descricao: str | None = None
    preco_compra: Decimal = Field(default=Decimal("0"), ge=0)
    preco_venda: Decimal = Field(default=Decimal("0"), ge=0)
    quantidade: int = Field(default=0, ge=0)
    quantidade_minima: int = Field(default=0, ge=0)
    categoria_id: str | None = None
    fornecedor_id: str | None = None

    @field_validator("codigo", "nome")
    @classmethod
    def nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Campo não pode ser vazio")
        return v.strip()

    @field_validator("categoria_id", "fornecedor_id")
    @classmethod
    def vazio_para_none(cls, v: str | None) -> str | None:
        if v is not None and v.strip() == "":
            return None
        return v


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    codigo: str | None = None
    nome: str | None = None
    descricao: str | None = None
    preco_compra: Decimal | None = None
    preco_venda: Decimal | None = None
    quantidade: int | None = None
    quantidade_minima: int | None = None
    categoria_id: str | None = None
    fornecedor_id: str | None = None


class ProdutoResponse(ProdutoBase):
    id: str
    estoque_baixo: bool = False

    model_config = ConfigDict(from_attributes=True)
