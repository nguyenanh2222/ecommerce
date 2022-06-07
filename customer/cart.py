from decimal import Decimal
from typing import List

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from starlette import status

from project.core.schemas import DataResponse
from project.core.swagger import swagger_response


class CartItemReq(BaseModel):
    amount: Decimal = Field(...)


class CartRes(BaseModel):
    item: List[CartItemReq] = Field([])


router = APIRouter()


@router.get(
    path="/",
    description="Get giỏ hàng của customer",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_cart(customer_id: int = Query(...)):
    return DataResponse(data=None)


@router.put(
    path="/items",
    description="Thêm một item vào giỏ hàng",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def add_item_to_cart(customer_id: int = Query(...), item: CartItemReq = Body(...)):
    return DataResponse(data=None)
