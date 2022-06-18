

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer,
                         primary_key=True,
                         nullable=False)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    email = Column(String)
    username = Column(String)

    class Config:
        arbitrary_types_allowed = True

    # def __repr__(self):
    #     return """<Customer(password='%s',
    #     name='%s', phone='%s',
    #     address='%s',
    #     email='%s', username='%s')>""" % (
    #         self.name, self.sex, self.clas,
    #         self.grade, self.email, self.username)


class Products(Base):

    __tablename__ = "products"

    product_id = Column(Integer,
                        primary_key=True,
                        nullable=False)
    description = Column(String)
    category = Column(String)
    name = Column(String)
    price = Column(DECIMAL)
    quantity = Column(Integer)
    created_time = Column(DATE)


# class Cart:
#     __tablename__ = "cart"
#
#     customer_id = Column(Integer, primary_key=True)
#     cart_id = Column(Integer,
#                      ForeignKey("Customers.customer_id"),
#                      nullable=False)
#
#
# class CartItems:
#     __tablename__ = "cart_items"
#
#     cart_id = Column(Integer,
#                          ForeignKey("Cart.cart_id"),
#                          nullable=False)
#     product_name = Column(String)
#     cart_items_id = Column(Integer,
#                            primary_key=True,
#                            nullable=False)
#     product_id = Column(Integer,
#                         ForeignKey("Product.product_id"),
#                         nullable=False)
#     total_amount = Column(DECIMAL)
#     quantity = Column(Integer)
#     price = Column(DECIMAL)
#
#
class Orders:
    __tablename__ = "orders"

    order_id = Column(Integer,
                      primary_key=True,
                      nullable=False)
    customer_id = Column(Integer,
                         ForeignKey("Customers.customer_id"),
                         nullable=False)
    total_amount = Column(DECIMAL)
    status = Column(String)
    time_open = Column(DATE)


class OrderItems:

    __tablename__ = "order_items"
    product_id = Column(Integer,
                        primary_key=True,
                        nullable=False)
    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(DECIMAL)
    total_amount = Column(DECIMAL)
    order_id = Column(Integer,
                      ForeignKey("Order.order_id"),
                      nullable=True)
    order_items_id = Column(Integer,
                            primary_key=True,
                            nullable=False)
#


