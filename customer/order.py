import math
from decimal import Decimal

from fastapi import APIRouter, Query, Body, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status


from database import SessionLocal
from project.core.schemas import PageResponse, Sort, DataResponse
from project.core.swagger import swagger_response
from datetime import datetime
import order_status

from customer.cart import CartRes, CartItemsRes, CartItemReq


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
        customer_id: int = Query(..., description="Mã khách hàng hiện tại"),
        order_id: int = Query(None, description="Mã đơn hàng"),
        product_name: str = Query(None, description="Tên sản phẩm có trong đơn hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo hóa đơn asc|desc"),
):
    session = SessionLocal()
    query = f"""SELECT * FROM ecommerce.orders o
        JOIN ecommerce.order_items oi ON o.order_id = oi.order_id """
    parameters = [order_id, product_name, customer_id]
    for parameter in parameters:
        if parameter is not None:
            query += " WHERE "
            break
    if order_id is not None:
        query += f"order_id = {order_id} AND"
    if customer_id is not None:
        query += f" customer_id = {customer_id} AND"
    if product_name is not None:
        query += f" product_name LIKE '%{product_name}%' AND"
    if query.endswith("AND"):
        query = query[:-3]
    if sort_direction is not None:
        query += f"ORDER BY time_open {sort_direction}"
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


@router.post(
    path="{customer_id}/",
    status_code=status.HTTP_201_CREATED,
    description="Chốt đơn, tạo đơn hàng bao gồm luôn các order_item.",
    responses=swagger_response(
        response_model=DataResponse[OrderRes],
        success_status_code=status.HTTP_201_CREATED

    )
)
async def place_order(
        customer_id: int = Query(...),
        order: OrderReq = Body(...)
):
    session = SessionLocal()

    # insert into orders
    query = f""" INSERT INTO ecommerce.orders (customer_id)
    VALUES ({customer_id}) RETURNING *"""
    _rs: CursorResult = session.execute(query)
    order_id = _rs.fetchone()[0]

    # insert items into order_items
    query = f"""SELECT product_id, product_name,
    quantity, price, total_price
    FROM cart c
    JOIN cart_items ci
    ON c.cart_id = ci.cart_id
    JOIN orders o
    ON c.customer_id = o.customer_id
    WHERE c.customer_id = {customer_id} 
    AND order_id = {order_id}"""
    _rs: CursorResult = session.execute(query)
    result = _rs.fetchall()
    query = f""" INSERT INTO order_items
    (product_id, product_name, quantity, 
    price, total_price, order_id) VALUES """
    for item in result:
        query += f"""({item[0]}, '{item[1]}',
        {item[2]}, {item[3]}, {item[4]}, {order_id}) ,"""
    query = f"{query[:-1]} RETURNING *"
    _rs: CursorResult = session.execute(query)

    query = f"""SELECT SUM(total_price) 
    FROM cart_items ci 
    JOIN cart c
    ON ci.cart_id = c.cart_id
    WHERE customer_id = {customer_id}"""
    _rs: CursorResult = session.execute(query)
    order.total_amount = _rs.first()[0]
    _rs: CursorResult = session.execute(
        f""" INSERT INTO ecommerce.orders
        (customer_id ,total_amount, status, time_open)
        VALUES ({customer_id}, {order.total_amount},
        '{order_status.EOrderStatus.OPEN_ORDER}',
        '{order.time_open}') RETURNING *"""
    )
    result = _rs.fetchall()

    # subtraction product quantity
    query = f"""SELECT ci.product_id, SUM(ci.quantity)
                FROM cart_items ci
                JOIN cart c
                ON c.cart_id  = ci.cart_id
                WHERE customer_id = {customer_id}
                GROUP BY ci.product_id
                """
    _rs: CursorResult = session.execute(query)
    quans_cart = _rs.fetchall()
    for item in quans_cart:
        query = f""" SELECT p.product_id, p.quantity
        FROM ecommerce.products p 
        JOIN ecommerce.order_items oi2
        ON oi2.product_id = p.product_id
        WHERE p.product_id = {item[0]}
    """
        _rs: CursorResult = session.execute(query)
    quans_product = _rs.fetchall()

    # update product
    for item_c in quans_cart:
        for item_p in quans_product:
            if item_p[0] == item_c[0]:
                sub_product = item_p[1] - item_c[1]
                if sub_product < 0:
                    return DataResponse(data="SOLD OUT!")
                query = f""" UPDATE products
                SET  quantity = {sub_product}
                WHERE product_id = {item_p[0]}"""
                _rs: CursorResult = session.execute(query)


    # delete item in cart_items
    query = f""" DELETE 
    FROM ecommerce.cart_items ci
    USING ecommerce.orders o
    WHERE customer_id = {customer_id} 
    """
    _rs: CursorResult = session.execute(query)
    session.commit()

    return DataResponse(data=result)