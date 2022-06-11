from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status
from starlette.responses import Response

from database import SessionLocal
from project.core.schemas import PageResponse, Sort, DataResponse
from project.core.swagger import swagger_response


class CartItemReq(BaseModel):
    unit_price: float = Field(...)
    quantity: int = Field(...)
    total_price: int = Field(...)
    product_id: int = Field(...)


class CartItemsRes(BaseModel):
    product_id: int = Field(None)
    customer_id: int = Field(None)

# @router.post
