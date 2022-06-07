from decimal import Decimal

from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from starlette import status

from project.core import PageResponse, Sort, DataResponse
from project.core.swagger import swagger_response


class OrderReq(BaseModel):
    amount: Decimal = Field(...)


class OrderRes(BaseModel):
    order_id: int = Field(...)
    amount: Decimal = Field(...)


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
    return PageResponse(data=[])


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
        order: OrderReq = Body(...)
):
    return PageResponse(data=[])
