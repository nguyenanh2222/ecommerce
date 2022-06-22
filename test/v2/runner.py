from test.v2.executor.admin import AdminAPIExecutor
from test.v2.executor.customer import CustomerAPIExecutor

class TestSimpleCase:
    executor_admin = AdminAPIExecutor()
    executor_customer = CustomerAPIExecutor()

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

    def test_admin_get_by_id_product(self):
        product = {
            "name": "string",
            "quantity": 0,
            "price": 0,
            "description": "string",
            "category": "string",
            "created_time": "2022-06-22T11:42:15.468Z"
        }
        self.executor_admin.put_product(product)

    def test_admin_delete_product(self):
        self.executor_admin.delete_product()

    def test_admin_get_order(self):
        self.executor_admin.get_order()

    def test_admin_put_order(self):
        self.executor_admin.put_order(2,"OPEN")

    def test_admin_analysis_total(self):
        self.executor_admin.get_analysis_revenue(2)


    def test_customer_get_profile(self):
        self.executor_customer.get_customer_by_id(2)

    def test_customer_put_profile(self):
        self.executor_customer.put_customer(2)

    def test_customer_post_profile(self):
        self.executor_customer.post_customer(1)

    def test_customer_get_order(self):
        self.executor_customer.get_orders()

    def test_customer_post_order(self):
        self.executor_customer.post_order(2)
        ...
    def test_customer_get_cart(self):
        self.executor_customer.get_carts()

    def test_customer_put_item_cart(self):
        self.executor_customer.put_item_cart()

    def test_get_product_by_id(self):
        self.executor_customer.get_product_by_id(2)

    def test_put_product(self):
        self.executor_customer.put_product(2)

