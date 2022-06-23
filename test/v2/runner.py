from datetime import date
from test.v2.executor.admin import AdminAPIExecutor
from test.v2.executor.customer import CustomerAPIExecutor


class TestSimpleCase:
    executor_admin = AdminAPIExecutor()

    def test_admin_get_products(self):
        self.executor_admin.get_products()

    def test_admin_get_product_by_id(self):
        self.executor_admin.get_produc_by_id(2)

    def test_admin_post_product(self):
        product = {
            "name": "product name",
            "quantity": 0,
            "price": 0,
            "description": "product description",
            "category": "jean",
            "created_time": "2022-06-22T11:27:26.453Z"
        }
        self.executor_admin.post_product(product)

    def test_admin_put_by_id_product(self):
        product = {
            "description": "string",
            "name": "string",
            "quantity": 0,
            "category": "string",
            "price": 0,
            "product_id": 6,
            "created_time": 1655917200
        }

        self.executor_admin.put_product(5, product)

    def test_admin_delete_product(self):
        self.executor_admin.delete_product(1)

    def test_admin_get_order(self):
        self.executor_admin.get_order(1, 20)

    def test_admin_put_order(self):
        self.executor_admin.put_order(2, "OPEN")

    def test_admin_analysis_total(self):
        self.executor_admin.get_analysis_revenue(
            date.fromisoformat('2021-06-17'),
            date.fromisoformat('2021-06-19'))

    def test_admin_analysis_line(self):
        self.executor_admin.get_analysis_line(
            date.fromisoformat('2021-06-17'),
            date.fromisoformat('2021-06-19')
        )

    executor_customer = CustomerAPIExecutor()

    def test_customer_get_profile(self):
        self.executor_customer.get_customer_by_id(2)

    def test_customer_put_profile(self):
        customer = {
            "name": "nguyenanh",
            "phone": "033456789",
            "address": "quan 7",
            "email": "anh@gmail.com",
            "username": "anh23652",
            "password": "256321"
        }
        self.executor_customer.put_customer(1, customer)

    def test_customer_post_profile(self):
        customer = {
            "name": "anh",
            "address": "quan 8",
            "username": "123anh",
            "phone": "0336985321",
            "password": "469ngah",
            "email": "123abgh"
        }
        self.executor_customer.post_customer(customer)

    def test_customer_get_order(self):
        self.executor_customer.get_orders(1, 1, 1)

    def test_customer_post_order(self):
        self.executor_customer.post_order_place_order(3)

    def test_customer_get_cart(self):
        self.executor_customer.get_cart(1)

    def test_customer_put_item_cart(self):
        cart_item = {
            "price": 0,
            "quantity": 0,
            "total_price": 0,
            "product_id": 2,
            "product_name": "string"
        }
        self.executor_customer.put_item_cart(1, cart_item)

    def test_get_product_by_id(self):
        self.executor_customer.get_product_by_id(2)

    def test_put_product(self):
        product = {
                "name": "string",
                "quantity": 0,
                "price": 0,
                "description": "string",
                "category": "string",
                "created_time": "2022-06-23T05:03:15.430Z"
        }
        self.executor_customer.put_product(7, product)

    def test_post_order(self):
        order = {
                    "total_amount": 0,
                    "time_open": "2022-06-23T08:17:07.736Z",
                    "status": "string"
                    }
        self.executor_customer.post_order(3, order)

