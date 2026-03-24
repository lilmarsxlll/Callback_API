from pydantic import BaseModel


class ReserveResponse(BaseModel):
    status: str
    message: str
    reservation_id: str | None


class ReserveRequest(BaseModel):
    reservation_id: str
    product_id: str
    quantity: int


class LoginRequest(BaseModel):
    username: str
    password: str


class HealthyResponse(BaseModel):
    status: str
    message: str
