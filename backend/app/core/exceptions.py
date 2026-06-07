from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Recurso não encontrado") -> None:
        super().__init__(status_code=404, detail=detail)


class BusinessError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=422, detail=detail)


class ConflictError(HTTPException):
    def __init__(self, detail: str = "Recurso já existe") -> None:
        super().__init__(status_code=409, detail=detail)
