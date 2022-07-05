import math

from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import update
from sqlalchemy.orm import Session, selectinload
from starlette import status

from database import SessionLocal
from order_status import EOrderStatus
from orm.models import Orders, OrderItems
from project.core.schemas import DataResponse, PageResponse, Sort
from project.core.swagger import swagger_response


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
        customer_id: int = Query(None, description="Mã khách hàng hiện tại"),
        order_id: int = Query(None, description="Mã đơn hàng"),
        product_name: str = Query(None, description="Tên sản phẩm có trong đơn hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo hóa đơn asc|desc"),
):
    session: Session = SessionLocal()
    query = session.query(
        Orders
    ).options(selectinload(Orders.order_items))
    if order_id:
        query = query.filter(Orders.order_id == order_id)
    if customer_id:
        query = query.filter(Orders.customer_id == customer_id)
    if order_id:
        query = query.filter(Orders.order_id == order_id)
    if product_name:
        query = query.filter(OrderItems.product_name.
                             like(f"%{product_name}%"))
    if sort_direction == "asc":
        query = query.order_by(Orders.time_open)
    if sort_direction == "desc":
        query = query.order_by(Orders.time_open).desc()
    total = query.all()
    total_page = math.ceil(len(total) / size)
    total_items = len(total)
    if page and size is not None:
        query.offset((page - 1) * size).limit(size)
    current_page = page
    result = query.all()
    return PageResponse(data=result,
                        total_page=total_page,
                        total_items=total_items,
                        current_page=current_page)


@router.put(
    path="/{id}",
    status_code=status.HTTP_201_CREATED,
    description="Changing status"
)
async def change_order_status(
        id: int = Path(..., description="Mã hóa đơn cần thay đổi trạng thái"),
        next_status: EOrderStatus = Query(..., description="Trạng thái đơn hàng muốn thay đổi"),
):
    session: Session = SessionLocal()
    _rs = session.query(Orders).filter(Orders.order_id == id).first()
    if _rs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    _rs = session.query(Orders).filter(
        Orders.order_id == id).update(
        {Orders.status: next_status},
        synchronize_session=False
    )
    session.flush()
    session.commit()
    _result = session.query(Orders).filter(Orders.order_id == id).all()
    return DataResponse(data=_result)

