from decimal import Decimal

from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status
from starlette.responses import Response

from database import SessionLocal
from project.core.schemas import PageResponse, Sort
from project.core.swagger import swagger_response
from datetime import datetime

class OrderReq(BaseModel):
    total_amount: Decimal = Field(...)
    total_order: int = Field(...)
    product_price: Decimal = Field(...)
    time_hire: datetime = Field(...)

class OrderRes(BaseModel):
    order_id: int = Field(None)
    total_amount: Decimal = Field(None)
    product_quantity: int = Field(None)
    unit_price: int = Field(None)
    customer_id: int = Field(None)


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
    _rs = "SELECT * FROM ecommerce.products"
    if order_id or product_name or customer_name:
        _rs += "WHERE"
    if product_name is not None:
        _rs += f" product_name LIKE '%{product_name}%' ORDER BY {sort_direction}"
    if customer_name is not None:
        _rs += f" product_id = {customer_name} ORDER BY {sort_direction}"
    if page and size is not None:
        _rs += f" LIMIT {size} OFFSET {(page - 1) * size} "
    _result: CursorResult = session.execute(_rs)
    session.commit()
    return PageResponse(data=_result.fetchall())
# ...................................
# Thong ke theo ngay thang chua lam xong