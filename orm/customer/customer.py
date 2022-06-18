from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from orm.models import Customer
from project.core.schemas import DataResponse

router = APIRouter()


class CustomerReq(BaseModel):
    name: str = Field(...)
    phone: str = Field(...)
    address: str = Field(...)
    email: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


@router.get(
    path="/all",
    deprecated=True
)
async def get_customers():
    session: Session = SessionLocal()
    return session.query(Customer).all()


@router.get(
    path="/{id}",
    deprecated=True
)
async def get_customer(id: int):
    session: Session = SessionLocal()
    return session.query(Customer).get(id)


@router.put(
    path="/{id}/update",
)
async def update_profile(customer_id: int,
                         customer: CustomerReq):
    session = SessionLocal()
    _rs = session.query(Customer).filter_by(customer_id=customer_id).first()
    _rs.name = customer.name
    _rs.phone = customer.phone
    _rs.email = customer.email
    _rs.password = customer.password
    _rs.username = customer.username
    session.commit()
    return session.query(Customer).get(customer_id)


@router.post(
    path="/{id}/insert"
)
async def create_profile(
        customer: CustomerReq
):
    session = SessionLocal()
    session.add(Customer(name=customer.name,
                         phone=customer.phone,
                         email=customer.email,
                         password=customer.password,
                         username=customer.username)
                )
    session.commit()
    return DataResponse(data="")


@router.delete(
    path="/delete",
    deprecated=True
)
async def delete_customer(
        customer_id: int
):
    session: Session = SessionLocal()
    _rs = session.get(Customer, customer_id)
    session.delete(_rs)
    session.commit()
    return DataResponse(data="")
