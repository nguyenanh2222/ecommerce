from test.v2.executor.admin import AdminAPIExecutor


class TestSimpleCase:
    executor = AdminAPIExecutor()

    def test_admin_get_products(self):
        self.executor.get_products()

    def test_admin_post_product(self):
        product = {
            "name": "product name",
            "quantity": 0,
            "price": 0,
            "description": "product description",
            "category": "jean",
            "created_time": "2022-06-22T11:27:26.453Z"
        }
        self.executor.post_product(product)
