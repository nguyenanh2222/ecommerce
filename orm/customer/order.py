import math

from datetime import datetime
from decimal import Decimal
from operator import or_

from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from sqlalchemy import asc, insert, func, select
from sqlalchemy.orm import Session, selectinload
from starlette import status

from database import SessionLocal
from orm.models import Products, Orders, OrderItems, Cart, CartItems
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
    session = SessionLocal()
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


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    description="creating orders, including order_items",
    responses=swagger_response(
        response_model=DataResponse[OrderRes],
        success_description=status.HTTP_201_CREATED
    )
)
async def place_order(
        customer_id: int = Query(...),
        order: OrderReq = Body(...)
):
    # insert into OrderItems
    session: Session = SessionLocal()
    stmt = insert(Orders).values(
            customer_id=f"{customer_id}",
            total_amount=f"{order.total_amount}",
            status=f"{order.status}",
            time_open=f"{order.time_open}").returning(
        Orders.order_id
    )

    session.execute(stmt)
    session.commit()

    # insert into OrderItems
    query = session.query(
        Orders.order_id,
        CartItems.product_id,
        CartItems.product_name,
        CartItems.total_price,
        CartItems.quantity,
        CartItems.price
    ).join(Cart, Orders.customer_id==Cart.customer_id).join(
        CartItems, CartItems.cart_id == Cart.cart_id).where(
        Orders.customer_id == customer_id
    ).all()

    for item in query:
        session.add(OrderItems(
                order_id=item[0],
                product_id=item[1],
                product_name=item[2],
                total_price=item[4] * item[5],
                quantity=item[4],
                price=item[5]
            ))
        session.execute(stmt)
        session.commit()

    query = session.query(
        Products.product_id, func.sum(Products.quantity)
    ).join(OrderItems,
           OrderItems.product_id == Products.product_id).join(
        Orders, Orders.order_id == OrderItems.order_id).filter(
        Orders.customer_id == customer_id).group_by(
        Products.product_id)
    p_in_order = query.all()
    print(p_in_order)
    query = session.query(
        OrderItems.product_id, func.sum(OrderItems.quantity)
    ).join(OrderItems,
           OrderItems.product_id == Products.product_id).join(
        Orders, Orders.order_id == OrderItems.order_id).filter(
        Orders.customer_id == customer_id).group_by(
        Products.product_id)
    query.all()
    p_in_product = query.all()
    print(p_in_product)
    # subtract product
    i
