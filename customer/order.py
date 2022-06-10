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
    time_hire: datetime = Field(...)
    status: str = Field(...)


class OrderRes(BaseModel):
    order_id: int = Field(...)
    customer_id: int = Field(...)
    total_amount: Decimal = Field(...)
    time_hire: datetime = Field(...)
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
    _rs: CursorResult = session.execute(f"""SELECT * FROM ecommerce.orders AS o
        RIGHT JOIN ecommerce.order_items AS oi ON o.order_id = oi.order_id """)
    if product_name or customer_id or order_id:
        _rs += "WHERE"
    if product_name is not None:
        _rs += f" product_name LIKE '%{product_name}% ORDER BY {sort_direction}'"
    if customer_id is not None:
        _rs += f" customer_name LIKE '%{customer_id}%' ORDER BY {sort_direction}"
    if order_id is not None:
        _rs += f" order_id = {order_id} ORDER BY {sort_direction}"
    if page and size is not None:
        _rs += f" LIMIT {size} OFFSET {(page - 1) * size} "
    session.commit()
    return PageResponse(data=_rs.fetchall())


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
        order: OrderReq = Body(...),

):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f""" INSERT INTO ecommerce.orders () 
        VALUES status = {order.status} 
        WHERE customer_id = {customer_id} RETURNING *"""
    )
    session.commit()
    return PageResponse(data=_rs.fetchall())
