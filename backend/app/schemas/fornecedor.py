from pydantic import BaseModel, ConfigDict, field_validator


class FornecedorBase(BaseModel):
    nome: str
    cnpj: str | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    descricao: str | None = None

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()

    @field_validator("cnpj")
    @classmethod
    def cnpj_formato(cls, v: str | None) -> str | None:
        if v is not None and v.strip() == "":
            return None
        return v


class FornecedorCreate(FornecedorBase):
    pass


class FornecedorUpdate(BaseModel):
    nome: str | None = None
    cnpj: str | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    descricao: str | None = None


class FornecedorResponse(FornecedorBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
