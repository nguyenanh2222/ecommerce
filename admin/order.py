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
    query = f"SELECT * FROM ecommerce.orders AS o " \
            f"LEFT JOIN ecommerce.customers  AS c on  o.customer_id = c.customer_id " \
            f"LEFT JOIN ecommerce.products  AS p ON o.product_id = p.product_id " \
            f"ORDER BY current_time {sort_direction}"

    if product_name or customer_name or order_id:
        query += "WHERE"
    if product_name is not None:
        query += f" product_name LIKE '%{product_name}%'"
    if customer_name is not None:
        query += f" customer_name LIKE '%{customer_name}%'"
    if order_id is not None:
        query += f" order_id = {order_id}"

    _rs = CursorResult = session.execute(query)
    result = []
    result.append(query)
    chunk = []
    for q in query:
        chunk.append(query)
    result = []
    while size < len(chunk):
        result = chunk[0: size + size]
        size += size
    result.append(chunk)
    page_len = len(query) % size
    result.append({'page': page_len})
    session.commit()
    return PageResponse(data=result)


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
        f"SELECT * CASE "
        f"WHEN status = {id}"
        f"THEN '{next_status}'"
        f"END "
        f"FROM ecommmerce.orders"
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
