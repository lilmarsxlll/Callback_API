from src.db import db
from fastapi import APIRouter, Depends, HTTPException
from src.models import Product, Reservation
from src.schemas import ReserveRequest, ReserveResponse
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth import get_current_user

import bcrypt

from src.schemas import LoginRequest
from src.models import User
from src.config.jwt_config import create_jwt_token

router = APIRouter()


@router.post("/reservation", response_model=ReserveResponse)
async def reserve_request(
    request: ReserveRequest,
    session: AsyncSession = Depends(db.get_session),
    current_user: str = Depends(get_current_user),
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
        await session.flush()

    return ReserveResponse(
        status="success",
        message=f"Reservation completed successfully by {current_user}.",
        reservation_id=reservation.reservation_id,
    )


@router.get("/reserve_status", response_model=ReserveResponse)
async def reserve_status(
    reservation_id: str,
    session: AsyncSession = Depends(db.get_session),
    current_user: str = Depends(get_current_user),
):
    async with session:
        result = await session.execute(
            select(Reservation).where(Reservation.reservation_id == reservation_id)
        )
        reservation = result.scalar_one_or_none()
        if reservation is None:
            return ReserveResponse(
                status="error",
                message="Reservation not found.",
                reservation_id=reservation_id,
            )
        return ReserveResponse(
            status="success",
            message=f"Reservation found for user {current_user}.",
            reservation_id=reservation_id,
        )


@router.delete("/reservation_delete", response_model=ReserveResponse)
async def reservation_delete(
    reservation_id: str,
    session: AsyncSession = Depends(db.get_session),
    current_user: str = Depends(get_current_user),
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
                message=f"Reservation deleted successfully by {current_user}.",
                reservation_id=reservation_id,
            )
        return ReserveResponse(
            status="error",
            message="The ids dont match.",
            reservation_id=reservation_id,
        )


@router.delete("/reservation_delete_all", response_model=ReserveResponse)
async def reservation_delete_all(
    session: AsyncSession = Depends(db.get_session),
    current_user: str = Depends(get_current_user),
):
    async with session.begin():
        await session.execute(delete(Reservation))

        return ReserveResponse(
            status="success",
            message=f"All reservations deleted by {current_user}.",
            reservation_id=None,
        )


@router.post("/login")
async def login(request: LoginRequest, session: AsyncSession = Depends(db.get_session)):

    result = await session.execute(
        select(User).where(User.username == request.username)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(request.password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_jwt_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
