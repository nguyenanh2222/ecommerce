from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from orm.models import Products
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response


class ProductReq(BaseModel):
    name: str = Field(...)
    quantity: int = Field(...)
    price: Decimal = Field(...)
    description: str = Field(...)
    category: str = Field(...)
    created_time: datetime = Field(...)


router = APIRouter()

#
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductReq],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_products():
    session: Session = SessionLocal()
    _rs = session.query(Products).all()
    return DataResponse(data=_rs)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses= swagger_response(
        response_model=DataResponse[ProductReq],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_product(id: int):
    session: Session = SessionLocal()
    _rs = session.query(Products).get(id)
    return DataResponse(data=_rs)


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductReq],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_product(product_id: int, product: ProductReq):
    session: Session = SessionLocal()
    _rs = session.query(Products).filter_by(product_id=product_id).first()
    _rs.name = product.name
    _rs.price = product.price
    _rs.category = product.category
    _rs.quantity = product.quantity
    _rs.description = product.description
    _rs.created_time = product.created_time
    session.commit()
    return session.query(Products).get(product_id)
