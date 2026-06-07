from pydantic import BaseModel, ConfigDict, field_validator


class CategoriaBase(BaseModel):
    nome: str
    descricao: str | None = None

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None


class CategoriaResponse(CategoriaBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
