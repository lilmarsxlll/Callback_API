from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db
from app.models import Product, Reservation
from schemas import ReserveRequest, ReserveResponse

router = APIRouter()


@router.post("/reservation", response_model=ReserveResponse)
async def reserve_request(
    request: ReserveRequest, session: AsyncSession = Depends(db.get_session)
):
    async with session.begin():
        product = await session.get(Product, request.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.available_quantity < request.quantity:
            return ReserveResponse(
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
    return ReserveResponse(
        status="success",
        message="Reservation completed successfully.",
        reservation_id=reservation.reservation_id,
    )


@router.get("/reserve_status", response_model=ReserveResponse)
async def reserve_status(
    reservation_id: str, session: AsyncSession = Depends(db.get_session)
):
    async with session.begin():
        result = await session.execute(
            select(Reservation).where(Reservation.reservation_id == reservation_id)
        )
        reservations = result.scalar_one_or_none()
        if reservations is None:
            return ReserveResponse(
                status="error",
                message="Not enough stock available.",
                reservation_id=reservation_id,
            )
        return ReserveResponse(
            status="success",
            message="Reservation completed successfully.",
            reservation_id=reservation_id,
        )


@router.delete("/reservation_delete", response_model=ReserveResponse)
async def reservation_delete(
    reservation_id: str, session: AsyncSession = Depends(db.get_session)
):
    async with session.begin():
        reservation = await session.get(Reservation, reservation_id)
        if reservation is None:
            return ReserveResponse(
                status="error",
                message="There is nothing to delete.",
                reservation_id=reservation_id,
            )
        if reservation.reservation_id == reservation_id:
            await session.delete(reservation)
            return ReserveResponse(
                status="success",
                message="Reservation deleted successfully.",
                reservation_id=reservation_id,
            )
        return ReserveResponse(
            status="error",
            message="The ids dont match.",
            reservation_id=reservation_id,
        )
