from typing import List

from fastapi import APIRouter, Body, Query, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import selectinload, Session

from starlette import status

from orm.models import Cart, CartItems, Customer, Products
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from database import SessionLocal

class CartReq(BaseModel):
    ...


class CartRes(BaseModel):
    items: List[CartReq] = Field([])
    product_id: int = Field(None)
    customer_id: int = Field(None)


class CartItemReq(BaseModel):
    price: float = Field(...)
    quantity: int = Field(...)
    total_price: int = Field(...)
    product_id: int = Field(...)
    product_name: str = Field(...)


class CartItemsRes(BaseModel):
    product_id: int = Field(None)
    customer_id: int = Field(None)


router = APIRouter()

@router.get(
    path="/",
    description= "Get item include cart by customer_iod",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_cart(
        customer_id: int = Query(...)):
    session = SessionLocal()
    query = session.query(
        Cart, CartItems
    ).filter(
        Cart.customer_id == customer_id
    ).join(
        CartItems, Cart.cart_id == CartItems.cart_id).all()

    return DataResponse(data=query)

@router.put(
    path="/items",
    description="Add Item To Cart",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def add_item_to_cart(
        customer_id: int = Query(...),
        item: CartItemReq = Body(...)
):
    session: Session = SessionLocal()
    _rs = session.query(Cart).filter(
        Cart.customer_id == customer_id).first()
    if _rs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    cart_item = CartItems(
        product_id=item.product_id,
        product_name=item.product_name,
        price=item.price,
        total_price=item.total_price,
        cart_id=_rs.cart_id
    )
    session.add(cart_item)
    session.flush()
    session.commit()
    session.refresh(cart_item)
    return DataResponse(data=cart_item)

