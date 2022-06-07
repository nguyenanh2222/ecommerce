from decimal import Decimal

from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import Response

from project.core.schemas import PageResponse, Sort
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
        order_id: int = Query(None, description="Mã đơn hàng"),
        product_name: str = Query(None, description="Tên sản phẩm có trong đơn hàng"),
        customer_name: str = Query(None, description="Tên khách hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo hóa đơn asc|desc")
):
    return PageResponse(data=[])


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    description="Thay đổi trạng thái của đơn hàng"
)
async def change_order_status(
        id: int = Path(..., description="Mã hóa đơn cần thay đổi trạng thái"),
        next_status: str = Query(..., description="Trạng thái đơn hàng muốn thay đổi"),
):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
