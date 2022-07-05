import datetime
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from orm.models import Customer, Cart, Products, Orders
from test.v2.executor.admin import AdminAPIExecutor
from test.v2.executor.customer import CustomerAPIExecutor


class TestSimpleCase:
    executor_admin = AdminAPIExecutor()

    def test_admin_get_products(self):
        self.executor_admin.get_products(
            1, 20, "ao", "ao", 1, Decimal(200000), Decimal(500000), 'asc')

    def test_admin_get_product_by_id(self):
        session: Session = SessionLocal()
        product = Products(
            description="ao cotton",
            category="ao",
            name="ao",
            price=400000,
            quantity=5
        )
        session.add(product)
        session.flush()
        session.commit()
        session.refresh(product)
        self.executor_admin.get_produc_by_id(product.product_id)
        session.delete(product)
        session.commit()

    def test_admin_get_product_by_id_existing(self):
        session: Session = SessionLocal()
        _rs = session.query(Products.product_id).all()
        _product_id = [item[0] for item in _rs]
        check = max(_product_id) + 1
        self.executor_admin.get_product_by_id_existing(check)

    def test_admin_put_product_bad_request(self):
        product = {
            "name": 123,
            "quantity": 0,
            "price": 0,
            "description": "string",
            "category": "string",
            "created_time": "2022-06-25T03:49:23.394Z"
        }
        session: Session = SessionLocal()
        _product = Products(
            description="ao cotton",
            category="ao",
            name="ao",
            price=400000,
            quantity=5
        )
        session.add(_product)
        session.flush()
        session.commit()
        session.refresh(_product)
        self.executor_admin.put_product_bad_request(
            _product.product_id,
            product)

    def test_admin_post_product(self):
        product = {
            "name": "string",
            "quantity": 0,
            "price": 0,
            "description": "string",
            "category": "string",
            "created_time": "2022-06-25T03:54:19.610Z"
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
        session: Session = SessionLocal()
        _product = Products(
            description="ao",
            category="xxxxxxx",
            name="ao",
            price=400000,
            quantity=5,
            created_time=datetime.date(2022, 6, 22)
        )
        session.add(_product)
        session.flush()
        session.commit()
        session.refresh(_product)
        self.executor_admin.put_product(_product.product_id, product)
        session.delete(_product)
        session.commit()

    def test_admin_put_product_existing(self):
        session: Session = SessionLocal()
        _rs = session.query(Products.product_id).all()
        _product_id = [item[0] for item in _rs]
        check = max(_product_id) + 1
        self.executor_admin.get_product_by_id_existing(check)

    def test_admin_put_product_bad_request(self):
        bad_body = {
            "name": 123,
            "quantity": 0,
            "price": 0,
            "description": "string",
            "category": "string",
            "created_time": "2022-06-25T03:49:23.394Z"
        }
        session: Session = SessionLocal()
        _product = Products(
            description="ao",
            category="xxxxxxx",
            name="ao",
            price=400000,
            quantity=5,
            created_time=datetime.date(2022, 6, 22)
        )
        session.add(_product)
        session.flush()
        session.commit()
        session.refresh(_product)
        self.executor_admin.put_product_bad_request(
            _product.product_id, bad_body)
        session.delete(_product)
        session.commit()

    def test_admin_delete_product(self):
        session: Session = SessionLocal()
        _rs = session.query(Products.product_id).all()
        check = _rs[1][0]
        self.executor_admin.delete_product(check)

    def test_admin_delete_product_existing(self):
        session: Session = SessionLocal()
        _rs = session.query(Products.product_id).all()
        check = max(_rs)[0] + 1
        self.executor_admin.delete_product_existing(check)

    def test_admin_get_order_by_page_size(self):
        self.executor_admin.get_order_page_size(1, 20)

    def test_admin_get_order_by_customer_order(self):
        session: Session = SessionLocal()
        order_id = session.query(Orders.order_id).all()
        customer_id = session.query(Customer.customer_id).all()
        self.executor_admin.get_order_customer_order_id(
            order_id[1][0], customer_id[1][0])

    def test_admin_get_product_sort_direction(self):
        session: Session = SessionLocal()
        product_id = session.query(Products.product_id).all()
        self.executor_admin.get_product_sort_direction(
            product_id[1][0], 'asc')
        # tại sao không tạo ra một order để update lại ???????????

    def test_admin_put_order(self):
        ...
        # session: Session = SessionLocal()
        # order = Orders(
        #     order_id=,
        #     customer_id=,
        #     total_amount=,
        #     status=,
        #     time_open=
        # )

        self.executor_admin.put_order(order_id[0][0], "OPEN")

    def test_admin_put_order_existing(self):
        session: Session = SessionLocal()
        _rs = session.query(Orders.order_id).first()
        check = _rs[0] + 1
        self.executor_admin.put_order_existing(check, "OPEN")


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
        new_customer = Customer()
        session = SessionLocal()
        session.add(
            new_customer
        )
        self.executor_customer.get_customer_by_id(new_customer.customer_id)
        session.query(Customer).filter(Customer.customer_id == new_customer.customer_id).delete()

    def test_customer_put_profile(self):
        customer = {
            "address": "quan 7",
            "customer_id": 24,
            "username": "string",
            "name": "string",
            "phone": "string",
            "email": "string",
            "password": "string"
        }
        session: Session = SessionLocal()
        _customer = Customer(
            name=customer["name"],
            phone=customer["phone"],
            address=customer["address"],
            email=customer["email"],
            username=customer["username"],
            password=customer["password"]
        )
        session.add(_customer)
        session.flush()
        session.commit()
        session.refresh(_customer)
        self.executor_customer.put_customer(_customer.customer_id, customer)
        session.query(Customer).filter(
            Customer.customer_id == _customer.customer_id
        ).delete(synchronize_session='evaluate')
        session.commit()

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
        session: Session = SessionLocal()

        _product = Products(
            description="ao cotton",
            category="a",
            name="ao",
            price="300000",
            quantity=10,
            created_time=date.fromisoformat('2021-06-17')
        )
        session.add(_product)
        session.flush()
        session.commit()
        session.refresh(_product)

        _customer = Customer(
            name="NguyenAn",
            phone="0334803109",
            address="quan 9",
            email="nguyenvienah@gmail.com",
            username="anh123",
            password="123"
        )
        session.add(_customer)
        session.flush()
        session.commit()
        session.refresh(_customer)

        _cart = Cart(customer_id=_customer.customer_id)
        session.add(_cart)
        session.commit()

        cart_item = {
            "price": 300000,
            "quantity": 1,
            "total_price": 300000,
            "product_id": _product.product_id,
            "product_name": "ao"
        }
        self.executor_customer.put_item_cart(_customer.customer_id, cart_item)

    def test_get_product_by_id(self):
        res = self.executor_customer.get_product_by_id(2)
        assert res.status_code == status.HTTP_200_OK

    def test_get_product_by_id_not_found(self):
        res = self.executor_customer.get_customer_by_id(-1)
        assert res.status_code == status.HTTP_404_NOT_FOUND

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
