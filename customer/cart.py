from decimal import Decimal
from typing import List

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status

from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from database import SessionLocal


class CartReq(BaseModel):
    ...


class CartRes(BaseModel):
    item: List[CartReq] = Field([])
    product_id: int = Field(None)
    customer_id: int = Field(None)


router = APIRouter()


@router.get(
    path="/",
    description="Get giỏ hàng của customer",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_cart(customer_id: int = Query(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f""" SELECT * FROM ecommerce.cart AS c 
        RIGHT JOIN ecommerce.customers AS c2
        ON c.customer_id = c2.customer_id 
        JOIN ecommerce.products AS p
        ON c.product_id = p.product_id
        WHERE c.customer_id = {customer_id}""")

    return DataResponse(data=_rs.first())



@router.put(
    path="/items",
    description="Thêm một item vào giỏ hàng",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def add_item_to_cart(
        product_id: int, customer_id: int = Query(...),
        item: CartItemReq = Body(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f"""SELECT cart_id, unit_price, total_products
    FROM ecommerce.cart AS c
    RIGHT JOIN ecommerce.customers AS c2
    ON c.customer_id = c2.customer_id
    JOIN ecommerce.products AS p
    ON c.product_id = p.product_id
    WHERE c.customer_id = {customer_id} and c.product_id = {product_id}"""
    )
    tup = _rs.fetchone()

    item.unit_price = int(tup[1])
    item.total_products = tup[2]
    item.total_price = tup[1]*tup[2]

    item.total_price = item.unit_price * item.total_products
    _rs: CursorResult = session.execute(f""" 
    INSERT INTO ecommerce.cart 
    VALUES unit_price = {item.unit_price}, 
    total_product = {item.total_products},
    total_price = {item.total_price}
    WHERE cart_id = {tup[0]}
    """)
    session.commit()
    return DataResponse(data=None)
