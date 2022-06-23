from fastapi import APIRouter, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from orm.models import Orders
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from datetime import datetime
from sqlalchemy.engine import CursorResult

router = APIRouter()


@router.get(
    path="/total",
    status_code=status.HTTP_200_OK,
    description="tính doanh thu theo một khoảng thời gian",
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK
    )
)
async def analysis_revenue_in_period(
        start_datetime: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d")),
        end_datetime: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d"))
):
    session: Session = SessionLocal()
    _rs = session.query(func.sum(Orders.total_amount),
                        func.avg(Orders.total_amount),
                        func.count(Orders.order_id),
                        func.count(Orders.customer_id)).filter(
        Orders.time_open >= f'{start_datetime}'
    ).filter(
        Orders.time_open <= f'{end_datetime}'
    ).group_by(Orders.order_id).all()
    return DataResponse(data=_rs)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description="line char",
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK
    )
)
async def line_chart(
        day_started: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d")),
        day_ended: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d"))
):
    session = SessionLocal()
    query = f""" SELECT time_open, SUM(total_amount) FROM ecommerce.orders
    WHERE time_open >= '{day_started}'
    AND time_open <= '{day_ended}' 
    GROUP BY time_open
    """
    _rs: CursorResult = session.execute(query)
    result = _rs.fetchall()
    session: Session = SessionLocal()
    _rs = session.query(Orders.time_open, func.sum(Orders.total_amount)).filter(
        Orders.time_open >= f'{day_started}',
        Orders.time_open <= f'{day_ended}'
    ).group_by(
        Orders.time_open
    ).all()
    return DataResponse(data=_rs)
