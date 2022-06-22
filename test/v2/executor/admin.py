from datetime import datetime
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
    def put_product(self, body: Dict):
        res = client.put("/api/v2/admin/product/{id}",
                         json=body)
        assert res.status_code == status.HTTP_200_OK
    def delete_product(self):
        res = client.delete("/api/v2/admin/product/{id}")
        assert res.status_code == status.HTTP_204_NO_CONTENT

    def get_order(self):
        res = client.get("/api/v2/admin/order/")
        return res.status_code == status.HTTP_200_OK
    def put_order(self, id: int, next_status: str):
        res = client.put(f"/api/v2/admin/order{id}")
        return res.status_code == status.HTTP_201_CREATED
    def get_analysis_revenue(self,
                             start_datetime: datetime,
                             end_datetime: datetime):
        start_datetime = '2021-11-29T00:00:00'
        end_datetime = '2021-11-29T00:00:00'
        res = client.get("/api/v2/admin/analysis/total")
        return res.status_code == status.HTTP_200_OK
    def get_analysis_line(self):
        res = client.get("/api/v2/admin/ananlysis/")
        return res.status_code == status.HTTP_200_OK



