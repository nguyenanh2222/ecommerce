from starlette import status

from test.client import client


class CustomerAPIExecutor:

    def get_customer_by_id(self, id: int):
        res = client.get(
            f"/api/v2/customer/customer{id}/profile")
        assert res.status_code == status.HTTP_200_OK

    def put_customer(self, customer_id: int):
        res = client.put(
            f"/api/v2/customer/customer{customer_id}/profile"
        )
        assert res.status_code == status.HTTP_200_OK

    def post_customer(self, id):
        res = client.post(
            f"/api/v2/customer{id}"
        )
        assert res.status_code == status.HTTP_201_CREATED

    def get_orders(self):
        res = client.get(f"/api/v2/customer/order")
        assert res.status_code == status.HTTP_200_OK

    def post_order(self, customer_id: int):
        res = client.post(f"/api/v2/customer/order")
        assert res.status_code == status.HTTP_201_CREATED

    def get_carts(self):
        res = client.get(f"/api/v2/customer/cart")
        assert res.status_code == status.HTTP_200_OK

    def put_item_cart(self):
        res = client.put(f"/api/v2/customer/art")
        assert res.status_code == status.HTTP_200_OK

    def get_product(self):
        res = client.get(f"/api/v2/customer/product")
        assert res.status_code == status.HTTP_200_OK

    def get_product_by_id(self, id: int):
        res = client.get(f"/api/v2/customer/product/{id}")
        assert res.status_code == status.HTTP_200_OK

    def put_product(self, id: int):
        res = client.put(f"/api/v2/customer/product/{id}")
        assert res.status_code == status.HTTP_200_OK
