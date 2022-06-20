from typing import List

from fastapi import APIRouter, Body, Query, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import selectinload

from starlette import status

from orm.models import Cart, CartItems
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from database import SessionLocal

class CartReq(BaseModel):
    ...


class CartRes(BaseModel):
    items: List[CartReq] = Field([])
    product_id: int = Field(None)
    customer_id: int = Field(None)


class CartItemReq(BaseModel):
    price: float = Field(...)
    quantity: int = Field(...)
    total_price: int = Field(...)
    product_id: int = Field(...)
    product_name: str = Field(...)


class CartItemsRes(BaseModel):
    product_id: int = Field(None)
    customer_id: int = Field(None)


router = APIRouter()

@router.get(
    path="'/",
    description= "Get item include cart by customer_iod",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_cart(
        customer_id: int = Query(...)):
    session = SessionLocal()
    query = session.query(
        Cart, CartItems
    ).filter(
        Cart.customer_id == customer_id
    ).join(
        CartItems, Cart.cart_id == CartItems.cart_id).all()

    return DataResponse(data=query)


