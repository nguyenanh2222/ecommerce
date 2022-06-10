from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status
from starlette.responses import Response

from database import SessionLocal
from project.core.schemas import PageResponse, Sort, DataResponse
from project.core.swagger import swagger_response
from customer.cart import CartItemReq

router = APIRouter()


class OrderItemsReq(BaseModel):
    customer_name: str = Field(...)
    product_name: str = Field(...)
    quantity: int = Field(...)
    unit_price: float = Field(...)
    total_price: float = Field(...)


class OrderItemsRes(BaseModel):
    product_id: int = Field(None)
    order_id: int = Field(None)
    customer_name: str = Field(None)
    product_name: str = Field(None)
    quantity: int = Field(None)
    unit_price: float = Field(None)
    total_price: float = Field(None)


@router.post(
    path="/items",
    status_code=status.HTTP_201_CREATED,
    description="New order items",
    responses=swagger_response(
        response_model=DataResponse[OrderItemsRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def add_order_items(item: OrderItemsReq = Body(...),
                          id: int = Query(...)):

    session = SessionLocal()

    item.unit_price = CartItemReq.unit_price
    item.total_price = CartItemReq.total_price
    item.quantity = CartItemReq.total_products

    item.total_price = item.unit_price * item.quantity

    _rs: CursorResult = session.execute(f"""INSERT INTO order_id, customer_id,  order_items
    (quantity, unit_price, total_price)
    VALUES quantity = {item.quantity},
    unit_price = {item.unit_price}, total_price = {item.total_price}""")
    session.commit()
    return DataResponse(data=None)
