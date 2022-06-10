from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult, Row
from starlette import status
from starlette.responses import Response

from admin.examples.product import product_create
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
    price: Decimal = Field(None)
    description: str = Field(None)
    category: str = Field(None)
    time_create: datetime = Field(...)


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def create_product(product: ProductReq = Body(..., example=product_create)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f"""INSERT INTO products (name, quantity, price, description, category) 
        VALUES ('{product.name}', {product.quantity}, {product.price},
                '{product.description}', '{product.category}') RETURNING product_id """
    )
    session.commit()
    print(_rs.scalar())
    return DataResponse(data=None)


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
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo sản phẩm asc|desc")
):
    session = SessionLocal()
    _rs = "SELECT * FROM ecommerce.products"
    if name or category or product_id or from_price or to_price:
        _rs += "WHERE"
    if name is not None:
        _rs += f" name LIKE '%{name}%' ORDER BY {sort_direction}"
    if product_id is not None:
        _rs += f" product_id = {product_id} ORDER BY {sort_direction}"
    if from_price and to_price is not None:
        _rs += f""" price BETWEEN {from_price} AND {to_price} 
        ORDER BY {sort_direction}"""
    if page and size is not None:
        _rs += f" LIMIT {size} OFFSET {(page-1)*size} "
    _result: CursorResult = session.execute(_rs)
    session.commit()
    return PageResponse(data=_result.fetchall())


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
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(id: int):
    session = SessionLocal()
    _rs = session.execute(f'DELETE  FROM products WHERE product_id = {id}')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
