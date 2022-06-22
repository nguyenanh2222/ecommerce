from typing import Dict

from starlette import status

from test.client import client


class AdminAPIExecutor:
    def get_products(self):
        res = client.get("/api/v2/admin/product")
        assert res.status_code == status.HTTP_200_OK

    def get_product(self):
        ...

    def post_product(self, body: Dict):
        res = client.post(
            "/api/v2/admin/product/",
            json=body
        )
        assert res.status_code == status.HTTP_201_CREATED

    def put_product(self):
        ...

    def delete_product(self):
        ...
