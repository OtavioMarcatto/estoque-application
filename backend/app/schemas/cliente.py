from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


class ClienteBase(BaseModel):
    codigo: str | None = None
    nome: str
    contrato: str | None = None
    data_do_pedido: date | None = None
    data_da_entrega: date | None = None
    descricao_do_pedido: str | None = None
    cnpj: str | None = None
    cpf: str | None = None
    ie: str | None = None
    rg: str | None = None
    endereco: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None
    celular: str | None = None
    email: str | None = None
    responsavel_legal: str | None = None
    cpf_responsavel_legal: str | None = None

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()

    @field_validator(
        "codigo", "contrato", "cnpj", "cpf", "ie", "rg", "endereco",
        "bairro", "cidade", "estado", "cep", "celular", "email",
        "responsavel_legal", "cpf_responsavel_legal", "descricao_do_pedido",
    )
    @classmethod
    def vazio_para_none(cls, v: str | None) -> str | None:
        if v is not None and str(v).strip() == "":
            return None
        return v


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    codigo: str | None = None
    nome: str | None = None
    contrato: str | None = None
    data_do_pedido: date | None = None
    data_da_entrega: date | None = None
    descricao_do_pedido: str | None = None
    cnpj: str | None = None
    cpf: str | None = None
    ie: str | None = None
    rg: str | None = None
    endereco: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None
    celular: str | None = None
    email: str | None = None
    responsavel_legal: str | None = None
    cpf_responsavel_legal: str | None = None


class ClienteResponse(ClienteBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
