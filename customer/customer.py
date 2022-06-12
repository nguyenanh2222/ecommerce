from fastapi import APIRouter, Body, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult, Row
from starlette import status

from database import SessionLocal
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response


class CustomerReq(BaseModel):

    payment_method: str = Field(...)
    password: str = Field(...)
    name: str = Field(...)
    phone: str = Field(...)
    address: str = Field(...)
    email: str = Field(...)
    username: str = Field(...)


class CustomerRes(BaseModel):

    payment_method: str = Field(None)
    password: str = Field(None)
    name: str = Field(None)
    phone: str = Field(None)
    address: str = Field(None)
    email: str = Field(None)
    username: str = Field(None)


router = APIRouter()


@router.post(
    path="/customer",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def create_product(customer: CustomerRes = Body(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f"""INSERT INTO customers (payment_method, 
        password, name, phone, address, email, username) 
        VALUES ('{customer.payment_method}', '{customer.password}', {customer.name},
        '{customer.phone}','{customer.email}' ,'{customer.username}') RETURNING *"""
    )
    session.commit()
    return DataResponse(data=_rs.first())


@router.get(
    path="/customer",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=PageResponse[CustomerReq],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_customer(
        page: int = Query(1, description="Trang"),
        size: int = Query(20, description="Kích thuớc 1 trang có bao nhiu sản phẩm"),
        customer_id: int = Query(None, description="ID khach hang"),
        name: str = Query(None, description="Loại ngành hàng"),
        sort_direction: Sort.Direction = Query(None, description="Chiều sắp xếp theo ngày tạo sản phẩm asc|desc")
):
    session = SessionLocal()
    _rs = "SELECT * FROM customers"
    if name or customer_id or page or size:
        _rs += "WHERE"
    if name is not None:
        _rs += f" name LIKE '%{name}%' ORDER BY {sort_direction}"
    if customer_id is not None:
        _rs += f" product_id = {customer_id} ORDER BY {sort_direction}"
    if page and size is not None:
        _rs += f" LIMIT {size} OFFSET {(page - 1) * size} "
    _result: CursorResult = session.execute(_rs)
    session.commit()
    return PageResponse(data=_result.fetchall())


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_customer_by_id(id : int):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f'SELECT * FROM customer WHERE customer_id = {id}')
    customer = _rs.first()
    return DataResponse(data=customer)


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_product(id: int, product: CustomerReq):
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

#
# @router.delete(
#     path="/{id_}",
#     responses=status.HTTP_204_NO_CONTENT
# )
# async def delete_product(id_: str = Path(...)):
#     session = SessionLocal()
#     _rs: CursorResult = session.execute(f'DELETE FROM products WHERE product_id = {id_}')
#     session.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


