import math
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.engine import CursorResult

from database import SessionLocal


router = APIRouter()
@router.get(
    "/myproduct"
)
def get_myproduct(
        customer_id: str
):
    session = SessionLocal()
    stmt = text("""Select orders.customer_id, orders.order_id
            From orders 
            Where orders.customer_id = :customer_id""")
    _rs: CursorResult = session.execute(stmt,
                                        {'customer_id': customer_id})
    # preparestatement
    return _rs.fetchall()

