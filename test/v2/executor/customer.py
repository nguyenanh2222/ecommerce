from typing import Dict

from starlette import status

from test.client import client


class CustomerAPIExecutor:

    def get_customer_by_id(self, id: int):
        res = client.get(
            f"/api/v2/customer/customer{id}/profile")
        assert res.status_code == status.HTTP_200_OK

    def put_customer(self, customer_id: int, body: Dict):
        res = client.put("/api/v2/customer/customer{id}/profile?customer_id=" + f"{customer_id}",
                         json=body)
        assert res.status_code == status.HTTP_200_OK

    def post_customer(self, body: Dict):
        res = client.post(
            "/api/v2/customer/{id}",
            json=body)
        assert res.status_code == status.HTTP_201_CREATED

    def get_orders(self, page: int, size: int, customer_id: int):
        res = client.get(f"/api/v2/customer/order/?page={page}&size={size}&customer_id={customer_id}")
        assert res.status_code == status.HTTP_200_OK

    def post_order_place_order(self, customer_id: int):
        res = client.post(f"/api/v2/customer/order/?customer_id={customer_id}")
        assert res.status_code == status.HTTP_201_CREATED

    def get_cart(self, id: int):
        res = client.get(f"/api/v2/customer/cart/?customer_id={id}")
        assert res.status_code == status.HTTP_200_OK

    def put_item_cart(self, customer_id: int, body: Dict):
        res = client.put(f"/api/v2/customer/cart/items?customer_id={customer_id}",
                         json=body)
        assert res.status_code == status.HTTP_200_OK

    def get_product(self):
        res = client.get(f"/api/v2/customer/product")
        assert res.status_code == status.HTTP_200_OK

    def get_product_by_id(self, id: int):
        res = client.get(f"/api/v2/customer/product/{id}")
        assert res.status_code == status.HTTP_200_OK

    def put_product(self, product_id: int, body: Dict):
        res = client.put("/api/v2/customer/product/{id}?product_id="+f"{product_id}",
                         json=body)
        assert res.status_code == status.HTTP_200_OK
