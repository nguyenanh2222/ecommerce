
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status
from starlette.responses import Response

from database import SessionLocal
from project.core.schemas import PageResponse, Sort
from project.core.swagger import swagger_response


class OrderReq(BaseModel):
    total_amount: Decimal = Field(...)
    total_order: int = Field(...)
    product_price: Decimal = Field(...)
    time_hire: datetime = Field(...)


class OrderRes(BaseModel):
    order_id: int = Field(...)
    total_amount: Decimal = Field(...)
    product_quantity: int = Field(...)
    unit_price: int = Field(...)
    customer_id: int = Field(...)


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
        order_id: int = Query(None, description="Mã đơn hàng"),
        product_name: str = Query(None, description="Tên sản phẩm có trong đơn hàng"),
        customer_name: str = Query(None, description="Tên khách hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo hóa đơn asc|desc")
):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f"""SELECT * FROM ecommerce.orders AS o
    RIGHT JOIN ecommerce.order_items AS oi ON o.order_id = oi.order_id """)
    if product_name or customer_name or order_id:
        _rs += "WHERE"
    if product_name is not None:
        _rs += f" product_name LIKE '%{product_name}% ORDER BY {sort_direction}'"
    if customer_name is not None:
        _rs += f" customer_name LIKE '%{customer_name}%' ORDER BY {sort_direction}"
    if order_id is not None:
        _rs += f" order_id = {order_id} ORDER BY {sort_direction}"
    if page and size is not None:
        _rs += f" LIMIT {size} OFFSET {(page-1)*size} "
    session.commit()
    return PageResponse(data=_rs.fetchall())


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    description="Thay đổi trạng thái của đơn hàng"
)
async def change_order_status(
        id: int = Path(..., description="Mã hóa đơn cần thay đổi trạng thái"),
        next_status: str = Query(..., description="Trạng thái đơn hàng muốn thay đổi"),
):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f""" UPDATE ecommerce.orders SET status = '{next_status}' WHERE order_id = {id} RETURNING *"""
    )
    session.commit()
    return PageResponse(data=_rs.fetchall())
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
