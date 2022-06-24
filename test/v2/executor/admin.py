from datetime import datetime, date
from decimal import Decimal
from typing import Dict

from starlette import status

from test.client import client


class AdminAPIExecutor:
    def get_products(self, page:int,
                     size: int, name: str,
                     category: str, product_id: int, to_price: Decimal,
                     from_price: Decimal, sort_direction: str):
        res = f"""/api/v1/products/?"""
        if page:
            res += f"page={page}&"
        if size:
            res += f"size={size}&"
        if name:
            res += f"name={name}&"
        if category:
            res += f"category={category}&"
        if product_id:
            res += f"product_id={product_id}&"
        if from_price:
            res += f"from_price={from_price}&"
        if to_price:
            res += f"to_price={to_price}&"
        if sort_direction:
            res += f"sort_direction={sort_direction}&"
        res = client.get(res[:-1])
        assert res.status_code == status.HTTP_200_OK

    def get_produc_by_id(self, id: int):
        res = client.get(f"/api/v2/admin/products/{id}")
        assert res.status_code == status.HTTP_200_OK

    def get_product_by_id_existing(self, id: int):
        res = client.get(f"/api/v2/admin/product/{id}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def put_product(self, id: int, body: Dict):
        res = client.put(f"/api/v1/products/{id}",
                         json=body)
        assert res.status_code == status.HTTP_200_OK

    def put_product_existing(self, id: int):
        res = client.put(f"/api/v1/products/{id}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def put_product_bad_request(self, id: int, body: Dict):
        res = client.put(f"/api/v1/products/{id}", json=body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def post_product(self, body: Dict):
        res = client.post("/api/v2/admin/product/", json=body)
        assert res.status_code == status.HTTP_201_CREATED

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