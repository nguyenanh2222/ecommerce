import math

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
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


@router.post(
    path="/{customer_id}/",
    status_code=status.HTTP_201_CREATED,
    description="creating orders, including order_items",
    responses=swagger_response(
        response_model=DataResponse[OrderRes],
        success_description=status.HTTP_201_CREATED
    )
)
async def place_order(
        customer_id: int = Query(...),

):
    session: Session = SessionLocal()
    # insert into OrderItems
    _rs = session.query(
        Orders.order_id,
        CartItems.product_id,
        CartItems.product_name,
        CartItems.total_price,
        CartItems.quantity,
        CartItems.price
    ).join(Cart, Orders.customer_id == Cart.customer_id).join(
        CartItems, CartItems.cart_id == Cart.cart_id).where(
        Orders.customer_id == customer_id)
    list_cart_items = []
    for item in _rs:
        _dict_rs = dict(zip(
            ['order_id', 'product_id', 'product_name', 'total_price', 'quantity', 'price']
            , item))
        list_cart_items.append(_dict_rs)
    for cart_item in list_cart_items:
        session.add(OrderItems(
            order_id=cart_item['order_id'],
            product_id=cart_item['product_id'],
            product_name=cart_item['product_name'],
            total_price=cart_item['total_price'],
            quantity=cart_item['quantity'],
            price=cart_item['price']
        ))
        session.commit()

    # update column quantity on products table
    query = session.query(
        Products.product_id, Products.quantity
    ).join(
        OrderItems, OrderItems.product_id == Products.product_id
    ).join(
        Orders, Orders.order_id == OrderItems.order_id
    ).filter(Orders.customer_id == customer_id)
    from_product = query.all()
    query = session.query(
        OrderItems.order_id, OrderItems.quantity
    ).join(
        Orders, Orders.order_id == OrderItems.order_id
    ).filter(Orders.customer_id == customer_id)
    from_order = query.all()

    for item_c in from_order:
        for item_p in from_product:
            if item_p[0] == item_c[0]:
                sub_product = item_p[1] - item_c[1]
                query = session.query(Products).filter_by(
                    product_id=item_p[0]).first()
                query.quantity = sub_product
                session.commit()

    # delete item in cart_items
    query = session.query(CartItems).join(
        Cart, Cart.cart_id == CartItems.cart_id).filter(
        Cart.customer_id == customer_id).all()
    for item in query:
        session.delete(item)
        session.commit()

    _rs = session.query(Orders).filter(
        Orders.customer_id == customer_id)
    return DataResponse(data=_rs.all())

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        success_status_code=status.HTTP_201_CREATED,
        response_model=DataResponse
    )
)
async def add_order(customer_id: int, order_req: OrderReq):
    session: Session = SessionLocal()
    order = Orders(
        customer_id=customer_id,
        time_open=order_req.time_open,
        total_amount=order_req.total_amount,
        status=order_req.status)
    session.add(order)
    session.commit()
    session.refresh(order)
    return DataResponse(data=order)