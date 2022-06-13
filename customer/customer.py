from fastapi import APIRouter, Body, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult, Row
from starlette import status

from database import SessionLocal
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response


class CustomerReq(BaseModel):
    customer_id: int = Field(None)
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
async def create_customer(customer: CustomerReq = Body(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f"""INSERT INTO customers (payment_method, 
        password, name, phone, address, email, username) 
        VALUES ('{customer.payment_method}', '{customer.password}', '{customer.name}',
        '{customer.phone}', '{customer.address}','{customer.email}' ,'{customer.username}') RETURNING *"""
    )
    _customer_id = _rs.first()[0]
    _rs: CursorResult = session.execute(
        f"""INSERT INTO cart (customer_id) VALUES({_customer_id})"""
    )
    session.commit()
    return DataResponse(data=status.HTTP_201_CREATED)



