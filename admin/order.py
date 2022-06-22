import math
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status

from database import SessionLocal
from order_status import EOrderStatus
from project.core.schemas import PageResponse, Sort, DataResponse
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
        page: int = Query(1, description="Page"),
        size: int = Query(20, description="Kích thuớc 1 trang có bao nhiu sản phẩm"),
        order_id: int = Query(None, description="Mã đơn hàng"),
        product_name: str = Query(None, description="Tên sản phẩm có trong đơn hàng"),
        customer_name: str = Query(None, description="Tên khách hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo hóa đơn asc|desc")
):

    query = f"""SELECT * FROM ecommerce.orders o
    JOIN ecommerce.order_items oi ON o.order_id = oi.order_id """
    parameters = [order_id, product_name, customer_name]
    for parameter in parameters:
        if parameter is not None:
            query += " WHERE "
            break
    if order_id is not None:
        query += f"order_id = {order_id} AND"
    if customer_name is not None:
        query += f" customer_name LIKE '%{customer_name}%' AND"
    if product_name is not None:
        query += f" product_name LIKE '%{product_name}%' AND"
    if query.endswith("AND"):
        query = query[:-3]
    if sort_direction is not None:
        query += f"ORDER BY time_hire {sort_direction}"
    session = SessionLocal()
    _rs: CursorResult = session.execute(query)
    total = _rs.fetchall()
    total_page = math.ceil(len(total) / size)
    total_items = len(total)
    query += f" LIMIT {size} OFFSET {(page - 1) * size}"
    _rs: CursorResult = session.execute(query)
    _result = _rs.fetchall()
    current_page = page
    session.commit()
    return PageResponse(data=_result,
                        total_page=total_page,
                        total_items=total_items,
                        current_page=current_page)


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    description="Thay đổi trạng thái của đơn hàng"
)
async def change_order_status(
        id: int = Path(..., description="Mã hóa đơn cần thay đổi trạng thái"),
        next_status: EOrderStatus = Query(..., description="Trạng thái đơn hàng muốn thay đổi"),
):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f""" UPDATE ecommerce.orders SET status = '{next_status}' WHERE order_id = {id} RETURNING *"""
    )
    result = _rs.fetchone()
    session.commit()
    return DataResponse(data=result)


