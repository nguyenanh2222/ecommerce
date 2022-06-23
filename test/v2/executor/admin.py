from datetime import datetime, date
from typing import Dict

from starlette import status

from test.client import client


class AdminAPIExecutor:
    def get_products(self):
        res = client.get("/api/v2/admin/product")
        assert res.status_code == status.HTTP_200_OK

    def get_produc_by_id(self, id: int):
        res = client.get(f"/api/v2/admin/product/{id}")
        assert res.status_code == status.HTTP_200_OK, res.status_code

    def post_product(self, body: Dict):
        res = client.post(
            "/api/v2/admin/product/",
            json=body
        )
        assert res.status_code == status.HTTP_201_CREATED

    def put_product(self, id: int, body: Dict):
        res = client.put(f"/api/v2/admin/product/{id}",
                         json=body)
        assert res.status_code == status.HTTP_200_OK

    def delete_product(self, id: int):
        res = client.delete(f"/api/v2/admin/product/{id}")
        assert res.status_code == status.HTTP_204_NO_CONTENT

    def get_order(self, page: int, size: int):
        res = client.get(f"/api/v2/admin/order/?page={page}&size={size}")
        return res.status_code == status.HTTP_200_OK

    def put_order(self, id: int, next_status: str):
        res = client.put(
            f"/api/v2/admin/order{id}?next_status={next_status}")
        return res.status_code == status.HTTP_201_CREATED

    def get_analysis_revenue(self,
                             start_datetime: date,
                             end_datetime: date):
        res = client.get(f"/api/v2/admin/analysis/total?start_datetime={start_datetime}&end_datetime{end_datetime}=")
        return res.status_code == status.HTTP_200_OK

    def get_analysis_line(self,
                          day_started: date,
                          day_end: date):
        res = client.get(f"/api/v2/admin/analysis/?day_started={day_started}&day_ended={day_end}")
        return res.status_code == status.HTTP_200_OK
