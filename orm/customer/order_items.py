from decimal import Decimal

from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status

from database import SessionLocal
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response

router = APIRouter()


class OrderItemsReq(BaseModel):
    customer_name: str = Field(...)
    product_name: str = Field(...)
    quantity: int = Field(...)
    price: Decimal = Field(...)
    total_price: Decimal = Field(...)


class OrderItemsRes(BaseModel):
    product_id: int = Field(None)
    order_id: int = Field(None)
    customer_name: str = Field(None)
    product_name: str = Field(None)
    quantity: int = Field(None)
    price: Decimal = Field(None)
    total_price: Decimal = Field(None)

