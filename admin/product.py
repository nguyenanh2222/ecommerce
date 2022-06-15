from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult, Row
from starlette import status
import math
from database import SessionLocal
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response


class ProductReq(BaseModel):
    name: str = Field(...)
    quantity: int = Field(...)
    price: Decimal = Field(...)
    description: str = Field(...)
    category: str = Field(...)
    created_time: datetime = Field(...)


class ProductRes(BaseModel):
    product_id: int = Field(None)
    name: str = Field(None)
    quantity: int = Field(None)
    price: float = Field(None)
    description: str = Field(None)
    category: str = Field(None)
    created_time: datetime = Field(None)


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def create_product(product: ProductReq = Body(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f"""INSERT INTO ecommerce.products (name, quantity, price, description, category, created_time) 
        VALUES ('{product.name}', {product.quantity}, {product.price},
                '{product.description}', '{product.category}', '{product.created_time}') RETURNING *"""
    )
    session.commit()
    return DataResponse(data=_rs.first())


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=PageResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_products(
        page: int = Query(1, description="Trang"),
        size: int = Query(20, description="Kích thuớc 1 trang có bao nhiu sản phẩm"),
        name: str = Query(None, description="Tên sản phẩm"),
        category: str = Query(None, description="Loại ngành hàng"),
        product_id: int = Query(None, description="Mã sản phẩm"),
        from_price: Decimal = Query(None, description="Khoảng giá giới hạn dưới"),
        to_price: Decimal = Query(None, description="Khoảng giá giới hạn trên"),
        sort_direction: Sort.Direction = Query('ASC', description="Chiều sắp xếp theo ngày tạo sản phẩm ASC|DESC")
):
    _rs = f" SELECT * FROM ecommerce.products WHERE"
    _category = f" category LIKE '{category}'"
    _product_id = f" product_id = {product_id}"
    _name = f" name LIKE '{name}'"
    _price = f" price BETWEEN {from_price} AND {to_price}"
    _sort = f" ORDER BY created_time {sort_direction}"
    _pagination = f" LIMIT {size} OFFSET {(page - 1)* size}"

    _q = [_category, _product_id, _name, _price]
    for index, item in enumerate(_q):
        for i in range(index+1, len(_q)):
            if _q[index].count('None') == 0 and _q[index].count('= None') == 0:
                _rs += item
                if _q[i].count('None') == 0 and _q[i].count('= None') == 0:
                    _rs += f" AND {_q[i]}"
            if _q[index].count('None') != 0:
                _rs += f"{_q[i]}"
    print(_rs)

@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_product(id: int):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f'SELECT * FROM products WHERE product_id = {id}')
    product: Row = _rs.first()
    print(type(product), dict(product))
    return DataResponse(data=product)


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_product(id: int, product: ProductReq):
    session = SessionLocal()
    _rs = session.execute(
        f""" UPDATE products
        SET description = '{product.description}', 
        category = '{product.category}', name = '{product.name}', 
        price = {product.price}, quantity = {product.quantity}, 
        created_time = '{product.created_time}' 
        WHERE product_id = {id} RETURNING *""")
    session.commit()
    return DataResponse(data=_rs.first())


@router.delete(
    path="/{id_}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(id_: int = Query(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f'DELETE FROM products WHERE product_id = {id_}')
    session.commit()
    return DataResponse(data=None, status_code=status.HTTP_204_NO_CONTENT)
