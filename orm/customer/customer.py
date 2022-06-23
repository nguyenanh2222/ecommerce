from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from orm.models import Customer, Cart
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response

router = APIRouter()


class CustomerReq(BaseModel):
    name: str = Field(...)
    phone: str = Field(...)
    address: str = Field(...)
    email: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


class CustomerRes(BaseModel):
    customer_id: int = Field(None)
    password: str = Field(None)
    name: str = Field(None)
    phone: str = Field(None)
    address: str = Field(None)
    email: str = Field(None)
    username: str = Field(None)


@router.get(
    path="/customer{id}/profile",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_customer(id: int):
    session: Session = SessionLocal()
    return session.query(Customer).get(id)


@router.put(
    path="/customer{id}/profile",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_profile(customer_id: int,
                         customer: CustomerReq):
    session: Session = SessionLocal()
    _rs = session.query(Customer).filter_by(customer_id=customer_id).first()
    if _rs == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    _rs.name = customer.name
    _rs.phone = customer.phone
    _rs.email = customer.email
    _rs.password = customer.password
    _rs.username = customer.username
    session.commit()
    result = session.query(Customer).get(customer_id)
    return DataResponse(data=result)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def create_profile(
        customer: CustomerReq
):
    session: Session = SessionLocal()
    customer = Customer(name=customer.name,
                        phone=customer.phone,
                        email=customer.email,
                        password=customer.password,
                        username=customer.username)
    session.add(customer)
    session.flush()
    session.commit()
    session.refresh(customer)

    cart = Cart(customer_id=customer.customer_id)
    session.add(cart)
    session.commit()
    return DataResponse(data=customer)