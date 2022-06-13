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
    price: Decimal = Field(...)
    total_price: Decimal = Field(...)


class OrderItemsRes(BaseModel):
    product_id: int = Field(None)
    order_id: int = Field(None)
    customer_name: str = Field(None)
    product_name: str = Field(None)
    quantity: int = Field(None)
    price: Decimal = Field(None)
    total_price: Decimal = Field(None)


@router.post(
    path="/items",
    status_code=status.HTTP_201_CREATED,
    description="New order items",
    responses=swagger_response(
        response_model=DataResponse[OrderItemsRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def add_order_items(item: OrderItemsRes = Body(...),
                          id: int = Query(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f"""SELECT order_id from orders WHERE customer_id = {id}""")
    print(_rs.fetchone())
    _rs: CursorResult = session.execute(f"""INSERT INTO ecommerce.order_items 
    (product_id, product_name, quantity, price, total_price, order_id)
    VALUES  ({item.product_id}, '{item.product_name}', {item.quantity}, 
    {item.price}, {item.total_price}, {item.order_id}) RETURNING *""")
    session.commit()
    return DataResponse(data=_rs.fetchall())
