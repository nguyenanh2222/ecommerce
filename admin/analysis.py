from decimal import Decimal

from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import Response

from project.core.schemas import PageResponse, Sort
from project.core.swagger import swagger_response


class OrderReq(BaseModel):
    total_amount: Decimal = Field(...)
    total_order: int = Field(...)
    product_price: Decimal = Field(...)
    time_hire: timestamp = Field(...)
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
    query = f" SELECT * FROM orders " \
            f"WHERE DateField >= '2010-01-01' " \
            f"AND DateField < '2012-01-01'"
   _rs: CursorResult= session.execute(query)
    return PageResponse(data=result)