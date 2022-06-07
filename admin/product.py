from decimal import Decimal

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status
from starlette.responses import Response

from admin.examples.product import product_create
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response

from database import SessionLocal


class ProductReq(BaseModel):
    name: str = Field(...)
    quantity: int = Field(...)
    price: Decimal = Field(...)
    description: str = Field(...)
    category: str = Field(...)


class ProductRes(BaseModel):
    # product_id: int = Field(...)
    # name: str = Field(...)
    # quantity: int = Field(...)
    # price: Decimal = Field(...)
    # description: str = Field(...)
    # category: str = Field(...)
    product_id: int = Field(None)
    name: str = Field(None)
    quantity: int = Field(None)
    price: Decimal = Field(None)
    description: str = Field(None)
    category: str = Field(None)


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
    _rs: CursorResult = session.execute(f"INSERT INTO products (name, quantity, price, description, category) "
                                        f"VALUES ('{product.name}', {product.quantity}, {product.price},"
                                        f"'{product.description}', '{product.category}')")
    session.commit()
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
        # page: int = Query(1, description="Trang"),
        # size: int = Query(20, description="Kích thuớc 1 trang có bao nhiu sản phẩm"),
        name: str = Query(None, description="Tên sản phẩm"),
        category: str = Query(None, description="Loại ngành hàng"),
        product_id: str = Query(None, description="Mã sản phẩm"),
        from_price: Decimal = Query(None, description="Khoảng giá giới hạn dưới"),
        to_price: Decimal = Query(None, description="Khoảng giá giới hạn trên"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo sản phẩm asc|desc")
):
    session = SessionLocal()
    query = "SELECT * FROM ecommerce.products"
    if name or category or product_id or from_price or to_price:
        query += "WHERE"
    if name is not None:
        query += f"NAME LIKE '%{name}%'"

    queries: CursorResult = session.execute(
        f"SELECT * FROM ecommerce.products WHERE name = '{name}' OPERATOR"
        f"(SELECT * FROM ecommerce.products WHERE product_id = {product_id})")
        # f"SELECT * FROM products WHERE price > {from_price} AND price < {to_price} IS NULL OR "
        # f"SELECT * FROM products ORDER BY time_create {sort_direction}")


    # result = []
    # result.append(queries)
    # chunk = []
    # for query in queries:
    #     chunk.append(query)
    # result = []
    # while size < len(chunk):
    #     result = chunk[0: size + size]
    #     size += size
    #     result.append(chunk)
    # result[{'page': len(queries4)%size}]
    session.commit()
    return PageResponse(data=queries)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_product(id: int):
    return DataResponse(data=None)


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_product(id: int):
    return DataResponse(data=None)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
