from decimal import Decimal

from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status

from database import SessionLocal
from project.core.schemas import PageResponse, Sort, DataResponse
from project.core.swagger import swagger_response
from datetime import datetime
import order_status


class OrderReq(BaseModel):
    total_amount: Decimal = Field(...)
    time_open: datetime = Field(...)
    status: str = Field(...)


class OrderRes(BaseModel):
    order_id: int = Field(...)
    customer_id: int = Field(...)
    total_amount: Decimal = Field(...)
    time_open: datetime = Field(...)
    status: str = Field(...)



router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=PageResponse[OrderRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_orders(
        page: int = Query(1, description="Trang"),
        size: int = Query(20, description="Kích thuớc 1 trang có bao nhiu sản phẩm"),
        customer_id: int = Query(..., description="Mã khách hàng hiện tại"),
        order_id: int = Query(None, description="Mã đơn hàng"),
        product_name: str = Query(None, description="Tên sản phẩm có trong đơn hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo hóa đơn asc|desc"),
):
    session = SessionLocal()
    _rs= f"""SELECT * FROM ecommerce.orders o
        JOIN ecommerce.order_items oi 
        ON o.order_id = oi.order_id """
    if product_name or customer_id or order_id:
        _rs += "WHERE"
    if product_name is not None:
        _rs += f" product_name LIKE '%{product_name}%' OR"
    if customer_id is not None:
        _rs += f" customer_id = {customer_id} "
    if order_id is not None:
        _rs += f" order_id = {order_id} "
    if sort_direction is not None:
        _rs += f"ORDER BY time_hire "
    if page or size is not None:
        _rs += f" LIMIT {size} OFFSET {(page - 1) * size} "
    _result: CursorResult = session.execute(_rs)
    session.commit()
    return PageResponse(data=_result.fetchall())


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    description="Chốt đơn",
    responses=swagger_response(
        response_model=DataResponse[OrderRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def place_order(
        customer_id: int = Query(...),
        order: OrderReq = Body(...)):
    session = SessionLocal()

    _rs: CursorResult = session.execute(
        f""" INSERT INTO ecommerce.orders 
        (customer_id ,total_amount, status, time_open)
        VALUES ({customer_id}, {order.total_amount}, 
        '{order_status.EOrderStatus.OPEN_ORDER}', 
        '{order.time_open}') RETURNING *"""
    )
    session.commit()
    return PageResponse(data=_rs.fetchall())
