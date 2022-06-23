from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from sqlalchemy import update
from sqlalchemy.orm import Session

from starlette import status
import math
from database import SessionLocal
from orm.models import Products
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
    session: Session = SessionLocal()
    session.add(Products(
        name=product.name,
        quantity=product.quantity,
        price=product.price,
        description=product.description,
        category=product.category,
        created_time=product.created_time
    ))
    session.commit()
    return DataResponse(data=status.HTTP_201_CREATED)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=PageResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_products(
        page: int = Query(1, description="Page"),
        size: int = Query(20, description="Size in a page"),
        name: str = Query(None, description="Name product"),
        category: str = Query(None, description="Category"),
        product_id: int = Query(None, description="Product ID"),
        from_price: Decimal = Query(None, description="From price"),
        to_price: Decimal = Query(None, description="To price"),
        sort_direction: Sort.Direction = Query(None, description="Filter by")
):
    session: Session = SessionLocal()
    query = session.query(Products)
    if name:
        query = query.filter(Products.name.like(f"%{name}%"))
    if category:
        query = query.filter(Products.category.like(f"%{category}%"))
    if product_id:
        query = query.filter(Products.product_id == product_id)
    if from_price:
        query = query.filter(Products.price >= from_price)
    if to_price:
        query = query.filter(Products.price <= to_price)
    if sort_direction == 'asc':
        query = query.order_by(Products.created_time)
    if sort_direction == 'desc':
        query = query.order_by(Products.created_time).desc()
    total = query.all()
    total_page = math.ceil(len(total) / size)
    total_items = len(total)
    if page and size is not None:
        query.offset((page - 1) * size).limit(size)
    current_page = page
    result = query.all()
    return PageResponse(data=result,
                        total_page=total_page,
                        total_items=total_items,
                        current_page=current_page)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_product(id: int):
    session: Session = SessionLocal()
    return DataResponse(data=session.query(Products).get(id))

@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK)
)
async def update_product(id: int, product: ProductReq):
    session: Session = SessionLocal()
    session.execute(update(Products).where(
        Products.product_id == id
    ).values(
        description=product.description,
        category=product.category,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        created_time=product.created_time
    ))
    session.commit()
    _rs = session.query(Products).filter(Products.product_id == id).first()
    return DataResponse(data=_rs)

@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(id: int = Query(...)):
    session: Session = SessionLocal()
    session.query(Products).filter(
        Products.product_id == id).delete(
        synchronize_session=False
    )
    session.commit()
    return DataResponse(data=None, status_code=status.HTTP_204_NO_CONTENT)