from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db
from app.models import Product, Reservation
from config.schemas import ReserveStatus, ReserveRequest

router = APIRouter()


@router.post("/reservation")
async def reserve_request(
    request: ReserveRequest, session: AsyncSession = Depends(db.get_session)
):
    async with session.begin():
        product = await session.get(Product, request.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.available_quantity < request.quantity:
            return ReserveStatus(
                status="error",
                message="Not enough stock available.",
                reservation_id=request.reservation_id,
            )

        product.available_quantity -= request.quantity

        reservation = Reservation(
            reservation_id=request.reservation_id,
            product_id=request.product_id,
            required_quantity=request.quantity,
        )
        session.add(reservation)
    return ReserveStatus(
        status="success",
        message="Reservation completed successfully.",
        reservation_id=reservation.reservation_id,
    )
