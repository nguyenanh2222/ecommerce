from decimal import Decimal
from typing import List

from fastapi import APIRouter, Body, Query, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status

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
    unit_price: float = Field(...)
    quantity: int = Field(...)
    total_price: int = Field(...)
    product_id: int = Field(...)


class CartItemsRes(BaseModel):
    product_id: int = Field(None)
    customer_id: int = Field(None)


router = APIRouter()


@router.get(
    path="/",
    description="Get giỏ hàng của customer",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_cart(customer_id: int = Query(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f""" 
    SELECT * FROM customers c JOIN cart ca 
    ON c.customer_id = ca.customer_id 
    JOIN cart_items ci  
    ON ca.cart_id = ci.cart_id 
    WHERE ca.customer_id = {customer_id}""")
    return DataResponse(data=_rs.fetchall())


@router.put(
    path="/items",
    description="Thêm một item vào giỏ hàng",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def add_item_to_cart(
        customer_id: int = Query(...),
        item: CartItemReq = Body(...)
):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f""" SELECT * FROM customers c
    RIGHT JOIN cart ca ON c.customer_id = ca.customer_id 
    WHERE ca.customer_id = {customer_id}""")
    if _rs.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    _rs_cart: CursorResult = session.execute(f"""
    SELECT cart_id FROM cart WHERE customer_id = {customer_id}""")
    _cart_id = int(_rs_cart.fetchone()[0])
    _item: CursorResult = session.execute(f"""INSERT INTO cart_items 
        (cart_id, quantity, total_price, unit_price, product_id) 
        VALUES ({_cart_id}, {item.quantity}, 
        {item.quantity * item.unit_price}, {item.unit_price}, {item.product_id})""")
    session.commit()

    return DataResponse(data=None)


class CartItemReq:
    pass
