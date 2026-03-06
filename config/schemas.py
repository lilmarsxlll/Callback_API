from pydantic import BaseModel


class ReserveStatus(BaseModel):
    status: str
    message: str
    reservation_id: str


class ReserveRequest(BaseModel):
    reservation_id: str
    product_id: str
    quantity: int
