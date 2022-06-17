
from fastapi import APIRouter, Query, Body, Path
from starlette import status

from database import SessionLocal
from project.core.schemas import PageResponse, Sort, DataResponse
from project.core.swagger import swagger_response
from datetime import datetime, timezone
from customer.order import OrderRes
from sqlalchemy.engine import CursorResult
router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description= "tính doanh thu theo một khoảng thời gian",
    responses=swagger_response(
        response_model=PageResponse[OrderRes],
        success_status_code=status.HTTP_200_OK
    )
)

async def analysis_revenue_in_period(
        start_datetime: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d")),
        end_datetime: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d")),
        product_id: int = Query(None)
):

    session = SessionLocal()
    # Sum total_amount in period time
    query = f"""SELECT SUM(total_amount), AVG(total_amount) 
    FROM ecommerce.orders 
    WHERE time_open >= '{start_datetime}' 
    AND time_open <= '{end_datetime}'
    """
    _rs: CursorResult = session.execute(query)
    revenue = _rs.fetchone()
    return DataResponse(data= revenue)




