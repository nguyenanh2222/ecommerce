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
    _rs= f"""SELECT * FROM ecommerce.orders o
        JOIN ecommerce.order_items oi 
        ON o.order_id = oi.order_id """
    if product_name or customer_id or order_id:
        _rs += "WHERE"
    if product_name is not None:
        _rs += f" product_name LIKE '%{product_name}%' OR"
    if customer_id is not None:
        _rs += f" customer_id = {customer_id} "
    if order_id is not None:
        _rs += f" order_id = {order_id} "
    if sort_direction is not None:
        _rs += f"ORDER BY time_hire "
    if page or size is not None:
        _rs += f" LIMIT {size} OFFSET {(page - 1) * size} "
    _result: CursorResult = session.execute(_rs)
    session.commit()
    return PageResponse(data=_result.fetchall())


@router.post(
    path="/",
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

    global sub_product
    session = SessionLocal()

    # insert into orders
    query = f""" INSERT INTO orders (customer_id)
    VALUES ({customer_id})"""
    _rs: CursorResult = session.execute(query)


    # insert items into order_items
    query = f"""SELECT product_id, product_name,
    quantity, price, total_price, order_id
    FROM cart c
    JOIN cart_items ci
    ON c.cart_id = ci.cart_id
    JOIN orders o
    ON c.customer_id = o.customer_id
    WHERE c.customer_id = {customer_id}"""
    _rs: CursorResult = session.execute(query)
    result = _rs.fetchall()
    query = f""" INSERT INTO order_items
    (product_id, product_name, quantity, 
    price, total_price, order_id) VALUES """

    for item in result:
        query += f"""({item[0]}, '{item[1]}',
        {item[2]}, {item[3]}, {item[4]}, {item[5]}) ,"""
        print(query)
    query = f"{query[:-1]} RETURNING *"
    _rs: CursorResult = session.execute(query)

    # calculate order.total_amount
    query = f"""SELECT SUM(total_price) FROM order_items oi
    JOIN orders o
    ON oi.order_id = o.order_id
    WHERE customer_id = {customer_id}
    """
    _rs: CursorResult = session.execute(query)
    total_amount = _rs.fetchone()[0]
    order.total_amount = total_amount
    _rs: CursorResult = session.execute(
        f""" INSERT INTO ecommerce.orders
        (customer_id ,total_amount, status, time_open)
        VALUES ({customer_id}, {order.total_amount},
        '{order_status.EOrderStatus.OPEN_ORDER}',
        '{order.time_open}') RETURNING *"""
    )
    result = _rs.fetchall()

    # delete item in cart_items
    query = f"""SELECT cart_id FROM cart 
    WHERE customer_id = {customer_id}"""
    _rs: CursorResult = session.execute(query)
    cart_id = _rs.first()[0]
    query = f""" DELETE FROM cart_items
    WHERE cart_id = {cart_id} """
    _rs: CursorResult = session.execute(query)




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
        FROM products
        JOIN order_items oi
        ON oi.product_id = p.product_id
        WHERE p.product_id = {item[0]}
    """
        _rs: CursorResult = session.execute(query)
    quans_product = _rs.fetchall()
    print(quans_product)

    # update product
    for item_c in quans_cart:
        for item_p in quans_product:
            if item_p[0] == item_c[0]:
                sub_product = item_p[1] - item_c[1]
                print(sub_product)
                query = f""" UPDATE products
                SET  quantity = {sub_product},
                WHERE product_id = {item_p[0]}"""
                _rs: CursorResult = session.execute(query)
    session.commit()
    return PageResponse(data=result)

# comfirted, complicate, cancelled